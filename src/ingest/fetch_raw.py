"""Unduh data mentah dari sumber publik ke data/raw/ beserta metadata sumber.

Script ini hanya mengambil dan menyimpan file apa adanya; parsing dilakukan di tahap terpisah.

Pemakaian (dari root repo):
    python -m src.ingest.fetch_raw portal-tkdd --tahun 2026
    python -m src.ingest.fetch_raw perpres-118-2025
"""

import argparse
import hashlib
import json
import re
import time
from datetime import datetime
from pathlib import Path

import requests

REPO_ROOT = Path(__file__).resolve().parents[2]
RAW_ROOT = REPO_ROOT / "data" / "raw"

USER_AGENT = "Mozilla/5.0 (EWS-DBH-Perikanan research prototype)"
TIMEOUT_DETIK = 60
JEDA_DETIK = 0.3  # jeda antarpermintaan agar tidak membebani portal
PERCOBAAN = 3

PORTAL_BASE = "https://djpk.kemenkeu.go.id/portal"
PORTAL_HALAMAN = f"{PORTAL_BASE}/data/tkdd"

PERPRES_118_HALAMAN = "https://jdih.kemenkeu.go.id/dok/perpres-118-tahun-2025/summary"
PERPRES_118_PDF = (
    "https://jdih.kemenkeu.go.id/api/download/"
    "8e793c08-65bd-4e79-93cb-1c7607126d86/2025perpres118.pdf"
)


def buat_folder_snapshot(sumber: str, waktu: datetime) -> Path:
    # Portal berubah dalam hari yang sama, jadi nama folder memuat jam pengambilan.
    folder = RAW_ROOT / sumber / waktu.strftime("%Y-%m-%dT%H%M%S")
    folder.mkdir(parents=True, exist_ok=False)
    return folder


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def ambil(session: requests.Session, url: str) -> bytes:
    galat = None
    for percobaan in range(1, PERCOBAAN + 1):
        try:
            resp = session.get(url, timeout=TIMEOUT_DETIK)
            resp.raise_for_status()
            return resp.content
        except requests.RequestException as e:
            galat = e
            time.sleep(2 * percobaan)
    raise RuntimeError(f"gagal setelah {PERCOBAAN} percobaan: {galat}")


def parse_opsi_provinsi(html: str) -> dict[str, str]:
    """Ambil pasangan kode → nama dari <select name="provinsi"> di halaman portal."""
    blok = re.search(r'<select[^>]*name="provinsi".*?</select>', html, re.S)
    if blok is None:
        raise ValueError('elemen <select name="provinsi"> tidak ditemukan di halaman portal')
    opsi = re.findall(r'<option value="([^"]*)"[^>]*>\s*([^<]*?)\s*</option>', blok.group(0))
    return {kode: nama for kode, nama in opsi if kode != "--"}


def parse_catatan_portal(html: str) -> str | None:
    """Kalimat sumber data di portal, mis. '... (CakLur) per tanggal 28 Oktober 2026'."""
    m = re.search(r"Berdasarkan data[^<]*?per tanggal\s+\d{1,2}\s+\w+\s+\d{4}", html)
    return m.group(0).strip() if m else None


def nama_file_tkdd(provinsi: str, pemda: str) -> str:
    prov = "semua" if provinsi == "--" else provinsi
    pd = "semua" if pemda == "--" else pemda
    return f"prov-{prov}_pemda-{pd}.xml"


def tulis_source_json(folder: Path, metadata: dict) -> None:
    (folder / "source.json").write_text(
        json.dumps(metadata, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


def fetch_portal_tkdd(tahun: int, session: requests.Session | None = None) -> Path:
    session = session or requests.Session()
    session.headers["User-Agent"] = USER_AGENT
    waktu = datetime.now().astimezone()
    # Halaman utama diambil dulu: bila gagal, tidak ada folder snapshot kosong yang tertinggal.
    html_bytes = ambil(session, PORTAL_HALAMAN)
    html = html_bytes.decode("utf-8", errors="replace")
    provinsi = parse_opsi_provinsi(html)

    folder = buat_folder_snapshot("portal-tkdd", waktu)
    berkas: list[dict] = []
    gagal: list[dict] = []

    def simpan(relpath: str, url: str, data: bytes) -> None:
        tujuan = folder / relpath
        tujuan.parent.mkdir(parents=True, exist_ok=True)
        tujuan.write_bytes(data)
        berkas.append({"path": relpath, "url": url, "sha256": sha256(data), "bytes": len(data)})

    simpan("halaman_tkdd.html", PORTAL_HALAMAN, html_bytes)

    target = [("--", "--")]
    for kode_prov in provinsi:
        url = f"{PORTAL_BASE}/pemda/{kode_prov}/{tahun}"
        try:
            data = ambil(session, url)
            daftar_pemda = json.loads(data)
        except (RuntimeError, ValueError) as e:
            gagal.append({"url": url, "galat": str(e)})
            continue
        simpan(f"pemda/prov-{kode_prov}.json", url, data)
        # "--" = agregat provinsi; kode lain = pemda (termasuk "00" = pemerintah provinsi).
        target += [(kode_prov, kode_pemda) for kode_pemda in daftar_pemda]
        time.sleep(JEDA_DETIK)

    for kode_prov, kode_pemda in target:
        url = f"{PORTAL_BASE}/csv?type=tkdd&tahun={tahun}&provinsi={kode_prov}&pemda={kode_pemda}"
        try:
            data = ambil(session, url)
        except RuntimeError as e:
            gagal.append({"url": url, "galat": str(e)})
            continue
        # Ekspor "csv" portal sebenarnya SpreadsheetML (Excel 2003 XML); selain itu dianggap gagal.
        if not data.lstrip().startswith(b"<?xml"):
            gagal.append({"url": url, "galat": "respons bukan SpreadsheetML XML"})
            continue
        simpan(f"tkdd/{nama_file_tkdd(kode_prov, kode_pemda)}", url, data)
        time.sleep(JEDA_DETIK)

    tulis_source_json(folder, {
        "sumber": "Portal Data SIKD DJPK — TKDD (alokasi & realisasi per jenis TKD)",
        "url": PORTAL_HALAMAN,
        "url_ekspor": f"{PORTAL_BASE}/csv?type=tkdd&tahun={{tahun}}&provinsi={{kode}}&pemda={{kode}}",
        "url_daftar_pemda": f"{PORTAL_BASE}/pemda/{{kode_provinsi}}/{{tahun}}",
        "tahun_anggaran": tahun,
        "tanggal_akses": waktu.isoformat(timespec="seconds"),
        "tanggal_snapshot": None,
        "catatan_portal": parse_catatan_portal(html),
        "kelompok_data": ["D1", "D2"],
        "catatan": (
            "Ekspor berformat SpreadsheetML (bukan CSV). Nilai dalam miliar rupiah dibulatkan 2 desimal "
            "(presisi ±Rp10 juta). Kode provinsi/pemda adalah kode DJPK, bukan kode Kemendagri. "
            "Realisasi kumulatif, tanpa rincian tahap/SP2D/rekening. Data berubah dalam hari yang sama. "
            "tanggal_snapshot belum diisi otomatis; lihat catatan_portal."
        ),
        "jumlah_berkas": len(berkas),
        "gagal": gagal,
        "berkas": berkas,
    })
    return folder


def fetch_perpres_118_2025(session: requests.Session | None = None) -> Path:
    session = session or requests.Session()
    session.headers["User-Agent"] = USER_AGENT
    waktu = datetime.now().astimezone()
    data = ambil(session, PERPRES_118_PDF)
    if not data.startswith(b"%PDF"):
        raise RuntimeError("respons bukan file PDF")

    folder = buat_folder_snapshot("perpres-118-2025", waktu)
    nama = "2025perpres118.pdf"
    (folder / nama).write_bytes(data)
    tulis_source_json(folder, {
        "sumber": "JDIH Kemenkeu — Perpres 118/2025 tentang Rincian APBN TA 2026 (fulltext)",
        "url": PERPRES_118_HALAMAN,
        "url_unduh": PERPRES_118_PDF,
        "tahun_anggaran": 2026,
        "tanggal_akses": waktu.isoformat(timespec="seconds"),
        "tanggal_snapshot": "2025-11-28",
        "kelompok_data": ["D1", "D12"],
        "catatan": (
            "Lampiran V.8 'Rincian DBH SDA Perikanan menurut Provinsi/Kabupaten/Kota TA 2026' ada di "
            "halaman PDF 1001-1017 (dalam ribuan rupiah; 547 baris termasuk baris 'Selisih Lebih'; "
            "JUMLAH NASIONAL 218.493.091). PDF hasil scan; lapisan teks OCR bawaan banyak salah baca "
            "angka dan nama, jangan dipakai langsung. tanggal_snapshot = tanggal penetapan Perpres."
        ),
        "berkas": [{"path": nama, "url": PERPRES_118_PDF, "sha256": sha256(data), "bytes": len(data)}],
    })
    return folder


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="sumber", required=True)
    p_portal = sub.add_parser("portal-tkdd", help="Snapshot Portal TKDD DJPK untuk semua provinsi & pemda")
    p_portal.add_argument("--tahun", type=int, default=2026)
    sub.add_parser("perpres-118-2025", help="PDF Perpres 118/2025 (Rincian APBN TA 2026)")
    args = parser.parse_args()

    if args.sumber == "portal-tkdd":
        folder = fetch_portal_tkdd(args.tahun)
    else:
        folder = fetch_perpres_118_2025()

    meta = json.loads((folder / "source.json").read_text(encoding="utf-8"))
    print(f"Tersimpan di {folder.relative_to(REPO_ROOT)} ({len(meta['berkas'])} berkas)")
    if meta.get("gagal"):
        print(f"PERINGATAN: {len(meta['gagal'])} permintaan gagal, lihat 'gagal' di source.json")


if __name__ == "__main__":
    main()
