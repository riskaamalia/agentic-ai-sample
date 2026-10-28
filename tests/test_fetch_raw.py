import json

import pytest
import requests

from src.ingest import fetch_raw

HTML_PORTAL = """
<select name="type"><option value="tkdd">TKDD</option></select>
<select name="provinsi" id="sel_provinsi">
  <option value="--">Semua Provinsi</option>
  <option value="01">Provinsi Aceh</option>
  <option value="10" selected>Provinsi Jawa Barat</option>
</select>
<p>Berdasarkan data SIKD Fitur Lacak Salur (CakLur) per tanggal 28 Oktober 2026</p>
"""


class FakeResponse:
    def __init__(self, content: bytes, status: int = 200):
        self.content = content
        self.status = status

    def raise_for_status(self):
        if self.status >= 400:
            raise requests.HTTPError(f"HTTP {self.status}")


class FakeSession:
    """Session palsu: memetakan URL ke isi respons, tanpa akses jaringan."""

    def __init__(self, routes: dict[str, FakeResponse]):
        self.routes = routes
        self.headers = {}

    def get(self, url, timeout):
        return self.routes.get(url, FakeResponse(b"", status=404))


@pytest.fixture
def raw_root(tmp_path, monkeypatch):
    monkeypatch.setattr(fetch_raw, "RAW_ROOT", tmp_path)
    monkeypatch.setattr(fetch_raw, "JEDA_DETIK", 0)
    monkeypatch.setattr(fetch_raw.time, "sleep", lambda _: None)
    return tmp_path


def test_parse_opsi_provinsi_mengabaikan_semua_provinsi():
    assert fetch_raw.parse_opsi_provinsi(HTML_PORTAL) == {"01": "Provinsi Aceh", "10": "Provinsi Jawa Barat"}


def test_parse_opsi_provinsi_gagal_jelas_bila_select_hilang():
    with pytest.raises(ValueError):
        fetch_raw.parse_opsi_provinsi("<html></html>")


def test_parse_catatan_portal():
    assert fetch_raw.parse_catatan_portal(HTML_PORTAL).endswith("per tanggal 28 Oktober 2026")
    assert fetch_raw.parse_catatan_portal("<html></html>") is None


def test_fetch_portal_mencatat_kegagalan_bukan_melewatinya(raw_root):
    base = fetch_raw.PORTAL_BASE
    xml = b'<?xml version="1.0"?><Workbook/>'
    csv = f"{base}/csv?type=tkdd&tahun=2026"
    routes = {
        fetch_raw.PORTAL_HALAMAN: FakeResponse(HTML_PORTAL.encode()),
        f"{base}/pemda/01/2026": FakeResponse(json.dumps({"00": "Provinsi Aceh", "01": "Kab. Aceh Barat"}).encode()),
        # pemda Jawa Barat sengaja tidak tersedia (404)
        f"{csv}&provinsi=--&pemda=--": FakeResponse(xml),
        f"{csv}&provinsi=01&pemda=00": FakeResponse(xml),
        f"{csv}&provinsi=01&pemda=01": FakeResponse(b"<html>error</html>"),
    }

    folder = fetch_raw.fetch_portal_tkdd(2026, session=FakeSession(routes))
    meta = json.loads((folder / "source.json").read_text(encoding="utf-8"))

    tersimpan = {b["path"] for b in meta["berkas"]}
    assert "tkdd/prov-semua_pemda-semua.xml" in tersimpan
    assert "tkdd/prov-01_pemda-00.xml" in tersimpan
    assert "tkdd/prov-01_pemda-01.xml" not in tersimpan  # respons HTML ditolak
    url_gagal = {g["url"] for g in meta["gagal"]}
    assert f"{base}/pemda/10/2026" in url_gagal
    assert f"{csv}&provinsi=01&pemda=01" in url_gagal
    assert meta["catatan_portal"].endswith("28 Oktober 2026")
    assert meta["tanggal_snapshot"] is None


def test_fetch_perpres_menolak_respons_bukan_pdf(raw_root):
    session = FakeSession({fetch_raw.PERPRES_118_PDF: FakeResponse(b"<html>login</html>")})
    with pytest.raises(RuntimeError):
        fetch_raw.fetch_perpres_118_2025(session=session)
    assert not any(raw_root.iterdir())  # tidak ada folder snapshot setengah jadi
