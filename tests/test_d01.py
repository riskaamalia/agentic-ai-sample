import json

import pandas as pd
import pytest

from src.tables import portal_tkdd
from src.tables.d01 import load_d01


def ekspor(*baris: tuple[str, str, str, str]) -> str:
    """Ekspor SpreadsheetML minimal seperti yang dihasilkan portal."""
    sel = lambda t: f'<Cell><Data ss:Type="String">{t}</Data></Cell>'
    rows = "".join(f"<Row>{''.join(sel(t) for t in b)}</Row>" for b in baris)
    return (
        '<?xml version="1.0" encoding="UTF-8"?><Workbook xmlns="urn:schemas-microsoft-com:office:spreadsheet" '
        'xmlns:ss="urn:schemas-microsoft-com:office:spreadsheet"><Worksheet ss:Name="Data Export"><Table>'
        f"{rows}</Table></Worksheet></Workbook>"
    )


HEADER = ("Akun", "Anggaran", "Realisasi", "Persentase")


@pytest.fixture
def snapshot(tmp_path, monkeypatch):
    monkeypatch.setattr(portal_tkdd, "REPO_ROOT", tmp_path)
    snap = tmp_path / "2026-10-28T120000"
    (snap / "pemda").mkdir(parents=True)
    (snap / "tkdd").mkdir()
    (snap / "source.json").write_text(json.dumps({"tahun_anggaran": 2026, "tanggal_akses": "2026-10-28T12:00:00+07:00"}))
    (snap / "pemda" / "prov-09.json").write_text(json.dumps({"00": "Provinsi DKI Jakarta", "--": "Semua pemda"}))
    (snap / "pemda" / "prov-10.json").write_text(json.dumps({"00": "Provinsi Jawa Barat", "17": "Kota Bandung", "--": "Semua pemda"}))
    (snap / "tkdd" / "prov-09_pemda-00.xml").write_text(ekspor(HEADER, ("DBH SDA Perikanan", "1,19 M", "0,95 M", "80.00")))
    (snap / "tkdd" / "prov-10_pemda-00.xml").write_text(ekspor(HEADER, ("DBH Cukai Hasil Tembakau", "290,20 M", "215,93 M", "74.41")))
    (snap / "tkdd" / "prov-10_pemda-17.xml").write_text(ekspor(HEADER, ("     Dana Bagi Hasil", "3,00 M", "2,00 M", "66.67"), ("         DBH SDA Perikanan", "0,25 M", "0,20 M", "80.00")))
    return snap


def test_miliar_ke_rupiah():
    assert portal_tkdd.miliar_ke_rupiah("0,25 M") == 250_000_000
    assert portal_tkdd.miliar_ke_rupiah("1.234,56 M") == 1_234_560_000_000
    assert portal_tkdd.miliar_ke_rupiah("0,00 M") == 0
    with pytest.raises(ValueError):
        portal_tkdd.miliar_ke_rupiah("0,25 T")


def test_load_d01_hanya_pemda_penerima(snapshot):
    df = load_d01(snapshot)

    assert list(df["Nama_Pemda"]) == ["Provinsi DKI Jakarta", "Kota Bandung"]
    assert list(df["Kode_Pemda_DJPK"]) == ["09.00", "10.17"]
    assert list(df["Total_Pagu_Rp"]) == [1_190_000_000, 250_000_000]
    assert df.attrs["pemda_tanpa_akun"] == 1  # Provinsi Jawa Barat


def test_load_d01_php_ppp_kosong_bukan_nol(snapshot):
    df = load_d01(snapshot)
    assert df["Pagu_PHP_Rp"].isna().all()
    assert df["Pagu_PPP_Rp"].isna().all()
    assert df["Total_Pagu_Rp"].dtype == pd.Int64Dtype()


def test_load_d01_gagal_bila_ekspor_pemda_hilang(snapshot):
    (snapshot / "tkdd" / "prov-10_pemda-17.xml").unlink()
    with pytest.raises(FileNotFoundError):
        load_d01(snapshot)
