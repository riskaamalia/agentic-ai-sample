"""D2 — Realisasi Penyaluran DBH SDA Perikanan (sumber sementara: snapshot Portal TKDD DJPK).

Portal hanya menyajikan realisasi kumulatif per pemda. Satu baris = satu pemda pada satu snapshot, sehingga
penambahan realisasi bisa dilacak dengan membandingkan snapshot dari waktu ke waktu.

Kolom D2 yang tidak tersedia di portal dibiarkan kosong (bukan nol): No_SP2D, Tgl_SP2D, Tgl_Masuk_RKUD,
Tahap, No_Rek_RKUD, Status. Rincian per transaksi ada di CakLur/OM-SPAN (perlu akses resmi).
"""

from pathlib import Path

import pandas as pd

from src.tables import portal_tkdd

AKUN = "DBH SDA Perikanan"

KOLOM = {
    "Kode_Pemda_DJPK": "string",
    "Nama_Pemda": "string",
    "Tahun": "Int64",
    "Waktu_Snapshot": "string",
    "Tanggal_Data_Portal": "string",
    "Realisasi_Kumulatif_Rp": "Int64",
    "Persen_Realisasi": "Float64",
    "No_SP2D": "string",
    "Tgl_SP2D": "string",
    "Tgl_Masuk_RKUD": "string",
    "Tahap": "Int64",
    "No_Rek_RKUD": "string",
    "Status": "string",
    "Teks_Realisasi_Portal": "string",
    "Berkas_Sumber": "string",
}

TIDAK_TERSEDIA = ["No_SP2D", "Tgl_SP2D", "Tgl_Masuk_RKUD", "Tahap", "No_Rek_RKUD", "Status"]


def load_d02(snapshots: list[Path] | None = None) -> pd.DataFrame:
    """Realisasi kumulatif per pemda untuk setiap snapshot lengkap, urut snapshot lalu kode pemda."""
    snapshots = snapshots or portal_tkdd.semua_snapshot()

    baris = []
    tanpa_akun_terbaru = 0
    for snapshot in snapshots:
        source = portal_tkdd.baca_source(snapshot)
        tanggal_portal = portal_tkdd.tanggal_data_portal(source.get("catatan_portal"))
        tanpa_akun_terbaru = 0
        for kode, nama, relpath, akun in portal_tkdd.akun_per_pemda(snapshot, AKUN):
            if akun is None:
                tanpa_akun_terbaru += 1
                continue
            baris.append({
                "Kode_Pemda_DJPK": kode,
                "Nama_Pemda": nama,
                "Tahun": source["tahun_anggaran"],
                "Waktu_Snapshot": source["tanggal_akses"],
                "Tanggal_Data_Portal": tanggal_portal.isoformat() if tanggal_portal else pd.NA,
                "Realisasi_Kumulatif_Rp": portal_tkdd.miliar_ke_rupiah(akun["Realisasi"]),
                "Persen_Realisasi": float(akun["Persentase"]),
                **{kolom: pd.NA for kolom in TIDAK_TERSEDIA},
                "Teks_Realisasi_Portal": akun["Realisasi"],
                "Berkas_Sumber": f"{snapshot.name}/{relpath}",
            })

    df = pd.DataFrame(baris, columns=list(KOLOM)).astype(KOLOM)
    df.attrs.update({
        "tabel": "D2",
        "judul": "Realisasi Penyaluran DBH SDA Perikanan per Pemda (kumulatif per snapshot)",
        "snapshot": [str(s.relative_to(portal_tkdd.REPO_ROOT)) for s in snapshots],
        "jumlah_snapshot": len(snapshots),
        "pemda_tanpa_akun": tanpa_akun_terbaru,
        "catatan": (
            "Realisasi kumulatif dibulatkan portal ke 0,01 M. Rincian SP2D, tanggal, tahap, rekening, dan "
            "status tidak tersedia di portal publik (perlu akses CakLur/OM-SPAN)."
        ),
    })
    return df
