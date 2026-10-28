# CLAUDE.md

Panduan kerja Claude Code untuk repo ini. Baca seluruhnya sebelum mulai bekerja.

## Proyek

**SIKD Cerdas HKPD — Simulator Alokasi (DSS) & EWS Penyaluran DBH SDA Perikanan** untuk DJPK Kemenkeu.
Dibangun sebagai mini SaaS yang berpotensi dikembangkan menjadi produk, dimulai dari satu jenis TKD
(DBH SDA Perikanan) dan dirancang agar bisa diperluas ke jenis TKD lain.

Deliverable yang dilayani:
- **Deliverable 1 — Model DSS & EWS:** arsitektur bisnis, data, aplikasi, teknologi, analitik, AI, dan tata kelola.
- **Deliverable 2 — Use Case & Prototype:** simulator alokasi dengan alur INPUT → PROSES → OUTPUT yang dapat didemonstrasikan.

## Sumber kebenaran

Google Sheet use case (sumber utama, selalu cek versi terbaru sebelum mengubah logika):
https://docs.google.com/spreadsheets/d/1Jq-YDB_jPE5kz40AsQTqY0xaK3vU6GDOJ0mOZ0pKyqU/edit

| Tab | Isi | Peran |
|---|---|---|
| `Kebutuhan Data Skenario 1` | Pertanyaan EWS, data D1–D12, parameter simulator, aturan R1–R7, log asumsi AS-xx, lokasi dokumen daerah | **Scope MVP — rujukan utama** |
| `Pengembangan Engine, UI dan ske` | Definition of Done, AC-01–AC-04, slide Deliverable 1/2 & Simulator Penentuan TKD | Kriteria penerimaan |

Komentar sel di sheet berisi sumber dan tanggal akses; ikut dibaca. Bila sheet dan kode berbeda, sheet menang
dan perbedaannya dicatat. Tab lama `Sheet1` sudah dihapus dan tidak lagi menjadi rujukan; beberapa komentar
sel masih menyebut "Sheet1" — anggap rujukan itu tidak berlaku.

## Scope MVP (Skenario 1, TA 2026)

**Pertanyaan utama EWS:** apakah setiap kab/kota menerima DBH Perikanan 2026 sesuai pagu, pada waktunya,
dan ke rekening RKUD yang benar? Jika tidak, apakah penyebabnya **wajar** (kurang/lebih bayar sah, penundaan
karena syarat salur) atau **anomali** (salah nominal, salah waktu, salah kirim)?

**Simulator:** PNBP T-1 (PPP + PHP) × porsi daerah → dibagi menjadi komposisi bagi hasil (menurut luas laut)
dan komposisi kinerja (menurut skor) → estimasi alokasi per daerah, perbandingan skenario, rekonsiliasi
terhadap pagu resmi (D12), dan jejak perhitungan.

**Aturan EWS R1–R7** didefinisikan di sheet (bagian 5). Kode harus memakai kode aturan yang sama (R1, R2, …)
dan setiap ambang dibaca dari konfigurasi, tidak di-hardcode.

**Acceptance criteria (tab 3):**
- AC-01: prototype runnable — engine deterministik, input UI, output & perbandingan skenario.
- AC-02: minimal satu jenis TKD berjalan end-to-end input → hasil → perbandingan skenario.
- AC-03: minimal satu skenario cocok dengan perhitungan acuan, atau selisihnya didokumentasikan.
- AC-04: vertical slice direview ML/BA, blocker demo ditindaklanjuti sebelum showcase.

## Fakta domain & status verifikasi

Jangan perlakukan item "belum terverifikasi" sebagai fakta. Saat memakainya di kode, tandai sebagai asumsi
(ID AS-xx) dan buat bisa dikonfigurasi.

| Item | Status |
|---|---|
| DBH Perikanan = 80% PNBP PPP + PHP untuk daerah (UU 1/2022) — AS-01 | Terverifikasi |
| Pagu memakai realisasi PNBP T-1 (PP 37/2023) — AS-04 | Terverifikasi |
| Penerima: kab/kota + provinsi yang tidak terbagi kab/kota otonom; 31.01 Kep. Seribu → 31 Pemprov DKI — AS-05 | Terverifikasi sebagian |
| Komposisi 90% bagi hasil / 10% kinerja (PMK 35/2026) — AS-02 | Dari ringkasan JDIH, pasal belum dicek |
| Bagi hasil proporsional luas wilayah laut — AS-03 | Rumus pasti belum diverifikasi |
| Jadwal & porsi 7 tahap salur DBH SDA (PMK 35/2026 Ps. 82) | Dikutip dari pemberitaan, belum dicek ke teks PMK |
| Ambang R3–R7 (5%, 7 hari, 14 hari, 10%, 50%) | Asumsi awal tim, perlu konfirmasi DJPK |

## Peta sumber data

| Data | Sumber | Status |
|---|---|---|
| D1 pagu per pemda | Portal TKDD DJPK (`portal/data/tkdd`, ekspor SpreadsheetML per pemda) | Terambil; dibulatkan 0,01 M; kode DJPK, bukan Kemendagri |
| D1 pagu presisi | Perpres 118/2025 Lampiran V.8, hlm. PDF 1001–1017 (ribuan rupiah) | PDF scan, lapisan OCR bawaan rusak; belum diekstrak |
| D2 realisasi | Portal TKDD — hanya kumulatif per pemda per snapshot | Terambil; SP2D/tanggal/tahap/rekening hanya di CakLur (SIKD NG) / OM-SPAN, wajib login → perlu akses resmi |
| Historis audited DJPK (`?page_id=41626`) | Excel alokasi/realisasi 2014–2025 | Hanya "DBH SDA" gabungan, tidak memisahkan Perikanan → tidak dipakai |

Temuan terbuka dan asumsi baru dicatat di log asumsi sheet (bagian 6), bukan di file ini.

## Ketersediaan data (penting)

Bedakan dengan tegas tiga kondisi ini di skema, pipeline, dan UI — jangan pernah menyamakannya:
- **Tidak tersedia** — sumber tidak publik / belum diperoleh (mis. D3, D7, D8, D10 saat ini).
- **Terlambat / belum diperbarui** — sumber ada tetapi snapshot terakhir lebih tua dari jadwal rilis.
- **Nol** — sumber menyatakan nilai realisasi 0.

Data per transaksi SP2D dan nomor rekening RKUD memerlukan akses internal OM-SPAN/SIKD; aturan yang
bergantung padanya (R2, sebagian R1/R3/R4) harus menyatakan "tidak dapat dievaluasi" bila data tidak ada,
bukan diam-diam lolos.

## Prinsip kerja

- **Satu tahap per waktu.** Kerjakan satu tahap, jelaskan alasan desain, jalankan pengujian, lalu tunggu
  persetujuan sebelum pindah ke tahap berikutnya. Jangan menulis banyak kode sekaligus.
- **Jangan mengarang** data, API, endpoint, regulasi, pasal, atau hasil evaluasi. Jika belum pasti, tulis
  "belum diverifikasi" dan sebutkan apa yang perlu dicek.
- **Data publik pemerintah dulu.** Untuk setiap sumber, verifikasi ketersediaan, granularitas, dan frekuensi
  pembaruan sebelum membangun pipeline-nya. Catat URL dan tanggal akses.
- **Urutan fondasi:** data pipeline → validasi data → rule engine & simulator deterministik → statistical
  baseline → baru AI agent.
- **Data uji** boleh sintetis, tetapi harus jelas berlabel fixture dan tidak pernah tampil sebagai data riil.
- **Traceability:** setiap angka keluaran harus bisa ditelusuri ke sumber, versi parameter, dan asumsi (AS-xx).
- **LLM bukan penentu risiko.** LLM membantu investigasi, merangkum bukti, dan menjelaskan alert. Status alert
  ditentukan rule engine / statistik. Setiap alert menyertakan bukti dan dapat ditinjau manusia.
- Hasil simulator adalah bahan analisis, **bukan** penetapan alokasi final (AS-07).

## Stack

- Python untuk backend dan data engineering.
- FastAPI (backend), Streamlit (dashboard MVP).
- Penyimpanan tahap awal: file di folder `data/` (belum memakai PostgreSQL). PostgreSQL/pgvector
  dipertimbangkan nanti bila kebutuhan multi-pengguna atau RAG muncul.
  - Isi `data/` **tidak masuk git** (kecuali `data/README.md` dan `data/raw/.gitkeep`); setiap orang mengambil
    snapshot sendiri lewat `src/ingest/fetch_raw.py`. Jangan mengunduh data mentah secara manual/ad hoc.
  - Data tabular (D1–D12) → **CSV**; parameter, ambang R1–R7, dan metadata sumber → **JSON**.
  - File asli disimpan apa adanya di `data/raw/<sumber>/<YYYY-MM-DDTHHMMSS>/` beserta `source.json` (URL,
    waktu akses, sha256). Nama folder memuat jam karena portal bisa berubah dalam hari yang sama.
  - CSV dibaca dengan skema eksplisit (dtype per kolom), tidak mengandalkan tebakan tipe pandas.
  - Nominal Rupiah disimpan sebagai bilangan bulat rupiah, bukan desimal/float.
  - Sel kosong = **tidak tersedia**; `0` = **nilai nol**. Saat membaca, matikan konversi NA default pandas
    selain sel kosong, dan jangan pernah mengisi kosong dengan 0. Kondisi "terlambat diperbarui" dicatat
    di metadata sumber (tanggal snapshot), bukan di sel data.
- LangGraph untuk orkestrasi AI agent — setelah fondasi siap.

## Perintah

Selalu dari root repo, memakai `.venv`, dan dengan `-m` (bukan path file) agar paket `src` dikenali:

```bash
.venv/bin/python -m src.ingest.fetch_raw portal-tkdd --tahun 2026   # snapshot portal, ±10 menit
.venv/bin/python -m src.ingest.fetch_raw perpres-118-2025           # PDF Perpres, ±21 MB
.venv/bin/streamlit run app.py                                      # http://localhost:8501/data
.venv/bin/python -m pytest
```

## Konvensi kode

- Alur: `src/ingest/` mengambil file mentah → `src/tables/` membaca file mentah menjadi DataFrame per kelompok
  data → `app.py` (Streamlit) menampilkannya.
- Tabel baru: buat `src/tables/dNN.py` berisi `load_dNN()` yang mengembalikan DataFrame dengan dtype eksplisit
  dan `df.attrs` (`tabel`, `judul`, `catatan`, info sumber), lalu daftarkan di `TABEL` pada `src/show_table.py`.
- Jangan memasang `if __name__ == "__main__"` di `src/tables/` maupun `src/show_table.py`; hanya `src/ingest/`
  yang dijalankan langsung dari terminal.
- Entry point dashboard adalah `app.py` di root; URL `/data` diatur lewat `.streamlit/config.toml`.
- Nama fungsi, variabel, dan kolom memakai Bahasa Indonesia, mengikuti nama field di sheet.
- Tes tidak boleh mengakses jaringan; pakai fixture sintetis di `tests/`.