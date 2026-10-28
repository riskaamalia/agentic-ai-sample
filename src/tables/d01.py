"""D1 — Pagu Definitif DBH SDA Perikanan per Kab/Kota (sumber sementara: snapshot Portal TKDD DJPK).

Keterbatasan sumber ini (lihat sheet use case, D1):
- Pagu dibulatkan portal ke 0,01 miliar, jadi Total_Pagu_Rp hanya presisi ±Rp5 juta.
- Portal tidak memisahkan PHP dan PPP, jadi Pagu_PHP_Rp dan Pagu_PPP_Rp kosong (tidak tersedia).
- Kode pemda adalah kode DJPK, bukan kode Kemendagri.
Angka presisi resmi ada di Perpres 118/2025 Lampiran V.8 (belum diekstrak).
"""

from pathlib import Path

import pandas as pd

from src.tables import portal_tkdd

AKUN = "DBH SDA Perikanan"

KOLOM = {
    "Kode_Pemda_DJPK": "string",
    "Nama_Pemda": "string",
    "Tahun": "Int64",
    "Pagu_PHP_Rp": "Int64",
    "Pagu_PPP_Rp": "Int64",
    "Total_Pagu_Rp": "Int64",
    "Teks_Pagu_Portal": "string",
    "Berkas_Sumber": "string",
}


def load_d01(snapshot: Path | None = None) -> pd.DataFrame:
    """Satu baris per pemda yang memiliki baris DBH SDA Perikanan di ekspor portal.

    Pemda tanpa baris tersebut (mis. pemprov yang bukan penerima) tidak dimasukkan; jumlahnya
    dicatat di df.attrs["pemda_tanpa_akun"].
    """
    snapshot = snapshot or portal_tkdd.snapshot_terbaru()
    source = portal_tkdd.baca_source(snapshot)
    tahun = source["tahun_anggaran"]

    baris = []
    tanpa_akun = []
    for kode_prov, kode_pemda, nama in portal_tkdd.daftar_pemda(snapshot):
        relpath = f"tkdd/prov-{kode_prov}_pemda-{kode_pemda}.xml"
        path = snapshot / relpath
        if not path.exists():
            raise FileNotFoundError(f"Ekspor untuk {nama} tidak ada di snapshot: {relpath}")
        akun = portal_tkdd.cari_akun(path, AKUN)
        if akun is None:
            tanpa_akun.append(nama)
            continue
        baris.append({
            "Kode_Pemda_DJPK": f"{kode_prov}.{kode_pemda}",
            "Nama_Pemda": nama,
            "Tahun": tahun,
            "Pagu_PHP_Rp": pd.NA,
            "Pagu_PPP_Rp": pd.NA,
            "Total_Pagu_Rp": portal_tkdd.miliar_ke_rupiah(akun["Anggaran"]),
            "Teks_Pagu_Portal": akun["Anggaran"],
            "Berkas_Sumber": relpath,
        })

    df = pd.DataFrame(baris, columns=list(KOLOM)).astype(KOLOM)
    df.attrs.update({
        "tabel": "D1",
        "judul": "Pagu DBH SDA Perikanan per Pemda",
        "snapshot": str(snapshot.relative_to(portal_tkdd.REPO_ROOT)),
        "tanggal_akses": source["tanggal_akses"],
        "catatan_portal": source.get("catatan_portal"),
        "pemda_tanpa_akun": len(tanpa_akun),
        "catatan": "Total_Pagu_Rp dibulatkan portal ke 0,01 M; PHP/PPP tidak tersedia di portal.",
    })
    return df
