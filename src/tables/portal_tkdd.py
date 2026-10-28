"""Baca snapshot mentah Portal TKDD DJPK (data/raw/portal-tkdd/...) tanpa mengubah file aslinya."""

import json
import re
import xml.etree.ElementTree as ET
from collections.abc import Iterator
from datetime import date
from decimal import Decimal, InvalidOperation
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
PORTAL_RAW = REPO_ROOT / "data" / "raw" / "portal-tkdd"

_SS = "{urn:schemas-microsoft-com:office:spreadsheet}"

_BULAN = {
    "januari": 1, "februari": 2, "maret": 3, "april": 4, "mei": 5, "juni": 6,
    "juli": 7, "agustus": 8, "september": 9, "oktober": 10, "november": 11, "desember": 12,
}


def semua_snapshot(root: Path = PORTAL_RAW) -> list[Path]:
    """Folder snapshot yang sudah lengkap (punya source.json), urut dari yang terlama."""
    lengkap = sorted(p.parent for p in root.glob("*/source.json"))
    if not lengkap:
        raise FileNotFoundError(
            f"Belum ada snapshot lengkap di {root}. Jalankan: python -m src.ingest.fetch_raw portal-tkdd"
        )
    return lengkap


def snapshot_terbaru(root: Path = PORTAL_RAW) -> Path:
    return semua_snapshot(root)[-1]


def tanggal_data_portal(catatan_portal: str | None) -> date | None:
    """'... per tanggal 28 Oktober 2026' → date(2026, 10, 28); None bila tidak terbaca."""
    if not catatan_portal:
        return None
    m = re.search(r"per tanggal\s+(\d{1,2})\s+(\w+)\s+(\d{4})", catatan_portal)
    if m is None or m.group(2).lower() not in _BULAN:
        return None
    return date(int(m.group(3)), _BULAN[m.group(2).lower()], int(m.group(1)))


def baca_baris(path: Path) -> list[list[str]]:
    """Isi ekspor SpreadsheetML portal sebagai daftar baris berisi teks sel (sudah di-strip)."""
    root = ET.parse(path).getroot()
    return [
        [(data.text or "").strip() for data in row.iter(f"{_SS}Data")]
        for row in root.iter(f"{_SS}Row")
    ]


def cari_akun(path: Path, akun: str) -> dict[str, str] | None:
    """Baris untuk satu akun (mis. 'DBH SDA Perikanan'); None bila akun tidak muncul di ekspor."""
    baris = baca_baris(path)
    header = baris[0]
    if header[:3] != ["Akun", "Anggaran", "Realisasi"]:
        raise ValueError(f"Header ekspor tidak dikenal di {path.name}: {header}")
    for sel in baris[1:]:
        if sel and sel[0] == akun:
            return dict(zip(header, sel))
    return None


def miliar_ke_rupiah(teks: str) -> int:
    """'1.234,56 M' → 1234560000000. Hasil mewarisi pembulatan portal (0,01 M = Rp10 juta)."""
    if not teks.endswith(" M"):
        raise ValueError(f"Satuan nilai portal tidak dikenal: {teks!r}")
    try:
        miliar = Decimal(teks[:-2].replace(".", "").replace(",", "."))
    except InvalidOperation as e:
        raise ValueError(f"Nilai portal tidak bisa dibaca: {teks!r}") from e
    rupiah = miliar * 1_000_000_000
    if rupiah != rupiah.to_integral_value():
        raise ValueError(f"Nilai portal tidak menghasilkan rupiah bulat: {teks!r}")
    return int(rupiah)


def daftar_pemda(snapshot: Path) -> list[tuple[str, str, str]]:
    """(kode_provinsi, kode_pemda, nama_pemda) untuk semua pemda di snapshot, kode DJPK."""
    hasil = []
    for path in sorted((snapshot / "pemda").glob("prov-*.json")):
        kode_prov = path.stem.removeprefix("prov-")
        for kode_pemda, nama in json.loads(path.read_text(encoding="utf-8")).items():
            if kode_pemda != "--":
                hasil.append((kode_prov, kode_pemda, nama))
    return hasil


def baca_source(snapshot: Path) -> dict:
    return json.loads((snapshot / "source.json").read_text(encoding="utf-8"))


def akun_per_pemda(snapshot: Path, akun: str) -> Iterator[tuple[str, str, str, dict[str, str] | None]]:
    """(kode_pemda_djpk, nama, relpath_ekspor, baris_akun) per pemda; baris_akun None bila akun tidak ada."""
    for kode_prov, kode_pemda, nama in daftar_pemda(snapshot):
        relpath = f"tkdd/prov-{kode_prov}_pemda-{kode_pemda}.xml"
        path = snapshot / relpath
        if not path.exists():
            raise FileNotFoundError(f"Ekspor untuk {nama} tidak ada di snapshot {snapshot.name}: {relpath}")
        yield f"{kode_prov}.{kode_pemda}", nama, relpath, cari_akun(path, akun)
