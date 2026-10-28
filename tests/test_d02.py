import json
from datetime import date

import pytest

from src.tables import portal_tkdd
from src.tables.d02 import TIDAK_TERSEDIA, load_d02
from tests.test_d01 import HEADER, ekspor


def buat_snapshot(root, nama, tanggal_akses, catatan, realisasi_bandung):
    snap = root / nama
    (snap / "pemda").mkdir(parents=True)
    (snap / "tkdd").mkdir()
    (snap / "source.json").write_text(json.dumps({
        "tahun_anggaran": 2026, "tanggal_akses": tanggal_akses, "catatan_portal": catatan,
    }))
    (snap / "pemda" / "prov-10.json").write_text(json.dumps({"00": "Provinsi Jawa Barat", "17": "Kota Bandung"}))
    (snap / "tkdd" / "prov-10_pemda-00.xml").write_text(ekspor(HEADER))
    (snap / "tkdd" / "prov-10_pemda-17.xml").write_text(
        ekspor(HEADER, ("DBH SDA Perikanan", "0,25 M", realisasi_bandung, "80.00"))
    )
    return snap


@pytest.fixture
def snapshots(tmp_path, monkeypatch):
    monkeypatch.setattr(portal_tkdd, "REPO_ROOT", tmp_path)
    return [
        buat_snapshot(tmp_path, "2026-09-01T080000", "2026-09-01T08:00:00+07:00",
                      "Berdasarkan data SIKD per tanggal 31 Agustus 2026", "0,15 M"),
        buat_snapshot(tmp_path, "2026-10-28T080000", "2026-10-28T08:00:00+07:00",
                      "Berdasarkan data SIKD per tanggal 28 Oktober 2026", "0,20 M"),
    ]


def test_tanggal_data_portal():
    assert portal_tkdd.tanggal_data_portal("... (CakLur)  per tanggal 28 Oktober 2026") == date(2026, 10, 28)
    assert portal_tkdd.tanggal_data_portal("per tanggal 5 Mei 2026") == date(2026, 5, 5)
    assert portal_tkdd.tanggal_data_portal("per tanggal 5 Bulan 2026") is None
    assert portal_tkdd.tanggal_data_portal(None) is None


def test_load_d02_satu_baris_per_pemda_per_snapshot(snapshots):
    df = load_d02(snapshots)

    assert list(df["Nama_Pemda"]) == ["Kota Bandung", "Kota Bandung"]
    assert list(df["Tanggal_Data_Portal"]) == ["2026-08-31", "2026-10-28"]
    assert list(df["Realisasi_Kumulatif_Rp"]) == [150_000_000, 200_000_000]
    assert df["Berkas_Sumber"].iloc[1] == "2026-10-28T080000/tkdd/prov-10_pemda-17.xml"
    assert df.attrs["jumlah_snapshot"] == 2
    assert df.attrs["pemda_tanpa_akun"] == 1


def test_load_d02_kolom_transaksi_kosong_bukan_nol(snapshots):
    df = load_d02(snapshots)
    for kolom in TIDAK_TERSEDIA:
        assert df[kolom].isna().all(), kolom
