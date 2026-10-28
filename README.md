# SIKD Cerdas HKPD — Simulator & EWS DBH SDA Perikanan

Prototype simulator alokasi (DSS) dan Early Warning System (EWS) penyaluran DBH SDA Perikanan untuk DJPK
Kemenkeu. Model awal memakai satu jenis TKD (DBH SDA Perikanan) dan dirancang agar bisa diperluas ke jenis TKD
lain.

**Status:** tahap awal. Sudah ada: script pengambil data mentah (Portal TKDD DJPK dan PDF Perpres 118/2025)
dan dashboard Streamlit yang menampilkan D1 (pagu DBH SDA Perikanan per pemda, dari portal). Belum ada rule
engine EWS, simulator, maupun review ML/BA. README ini bukan klaim bahwa Definition of Done sudah terpenuhi.

## Menjalankan

Semua perintah dari root repo, memakai Python 3.12 di `.venv`:

```bash
python3 -m venv .venv                      # sekali saja, bila .venv belum ada
.venv/bin/pip install pandas requests streamlit pytest   # dependensi (lihat pyproject.toml)

.venv/bin/python -m src.ingest.fetch_raw portal-tkdd --tahun 2026   # snapshot portal (±10 menit)
.venv/bin/python -m src.ingest.fetch_raw perpres-118-2025           # PDF Perpres (±21 MB)

.venv/bin/streamlit run app.py             # dashboard di http://localhost:8501/data
.venv/bin/python -m pytest                 # pengujian
```

Dashboard membaca snapshot lengkap terbaru di `data/raw/`; jalankan `fetch_raw` dulu bila folder itu masih
kosong. Struktur kode dijelaskan di [`src/README.md`](src/README.md).

## Sumber kebenaran

Use case, kebutuhan data, aturan EWS, log asumsi, dan acceptance criteria dikelola di Google Sheet:
https://docs.google.com/spreadsheets/d/1Jq-YDB_jPE5kz40AsQTqY0xaK3vU6GDOJ0mOZ0pKyqU/edit

- **Kebutuhan Data Skenario 1** — scope MVP: data D1–D12, parameter simulator, aturan R1–R7, asumsi AS-01–AS-07.
- **Pengembangan Engine, UI dan ske** — Definition of Done dan acceptance criteria AC-01–AC-04.

Panduan kerja (termasuk untuk Claude Code) ada di [`CLAUDE.md`](CLAUDE.md).

## Scope MVP — Skenario 1, TA 2026

**EWS penyaluran.** Apakah setiap kab/kota menerima DBH Perikanan 2026 sesuai pagu, pada waktunya, dan ke
rekening RKUD yang benar? Jika tidak, apakah selisihnya wajar (kurang/lebih bayar sah, penundaan karena syarat
salur belum dipenuhi) atau anomali (salah nominal, salah waktu, salah kirim)? Dijawab oleh tujuh aturan:

| Kode | Level | Kondisi |
|---|---|---|
| R1 | Merah | Total salur melebihi pagu |
| R2 | Merah | Salah kirim (kode daerah / rekening tidak cocok) |
| R3 | Oranye | Nominal tahap meleset padahal syarat salur lengkap |
| R4 | Oranye | Tahap terlambat padahal syarat salur lengkap |
| R5 | Kuning | Tahap tertunda karena daerah belum lapor |
| R6 | Kuning | Target DBH di APBD berbeda dari pagu pusat |
| R7 | Kuning | Dana sudah masuk tetapi serapan rendah (idle) |

Ambang setiap aturan masih asumsi awal dan perlu dikonfirmasi DJPK.

**Simulator alokasi.** INPUT (PNBP T-1, daftar daerah penerima, luas wilayah laut, indikator kinerja, pagu
historis) → PROSES (validasi kelengkapan, formula alokasi, simulasi perubahan parameter, rekonsiliasi terhadap
pagu) → OUTPUT (estimasi alokasi per daerah, perbandingan skenario, selisih terhadap pagu, jejak perhitungan).
Hasil simulator adalah bahan analisis, bukan penetapan alokasi final.

## Data

Sumber yang sudah diambil:

| Sumber | Dipakai untuk | Keterbatasan |
|---|---|---|
| Portal Data SIKD DJPK — TKDD | D1 (pagu), D2 (realisasi kumulatif) per pemda | Nilai dibulatkan 0,01 miliar; kode DJPK, bukan Kemendagri; tanpa rincian tahap/SP2D/rekening |
| Perpres 118/2025 Lampiran V.8 | Pagu presisi per pemda (ribuan rupiah) | PDF hasil scan; tabel belum diekstrak |

Sebagian data inti tidak tersedia di sumber publik (status syarat salur, posisi kas, PNBP T-1, luas wilayah
laut, dan transaksi SP2D per rekening); aturan yang bergantung padanya akan dilaporkan sebagai "tidak dapat
dievaluasi", bukan dianggap lolos.

Tahap awal tidak memakai database. Data disimpan sebagai file di folder `data/` dan **tidak masuk git**;
setiap anggota tim mengambil snapshot sendiri dengan script di atas. Detail konvensi ada di
[`data/README.md`](data/README.md).

```
data/
  raw/       file asli dari sumber, disimpan apa adanya + source.json (URL, waktu akses, sha256)
  ...        data tabular D1–D12 sebagai CSV; parameter, ambang, dan metadata sebagai JSON
```

Konvensi utama: nominal Rupiah sebagai bilangan bulat; sel kosong berarti **tidak tersedia**, `0` berarti
**nilai nol**; data yang terlambat diperbarui ditandai lewat tanggal snapshot di metadata sumber.

## Stack

- Python untuk pipeline data, validasi, rule engine, dan simulator deterministik.
- Streamlit untuk dashboard MVP (sudah dipakai); FastAPI untuk backend (rencana).
- LangGraph untuk AI agent setelah fondasi siap. LLM hanya membantu investigasi dan menjelaskan alert beserta
  buktinya; status risiko ditentukan rule engine dan dapat ditinjau manusia.

## Cara kerja

Pengembangan berjalan satu tahap per waktu: kerjakan satu tahap, jelaskan alasan desain, jalankan pengujian,
lalu review sebelum lanjut. Urutan fondasi: pipeline data → validasi data → rule engine & simulator → baseline
statistik → AI agent.

## Lisensi

Lihat [`LICENSE`](LICENSE).
