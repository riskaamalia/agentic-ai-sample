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
  - Data tabular (D1–D12) → **CSV**; parameter, ambang R1–R7, dan metadata sumber → **JSON**.
  - File asli dari portal disimpan apa adanya di `data/raw/` beserta metadata sumber (URL, tanggal akses).
  - CSV dibaca dengan skema eksplisit (dtype per kolom), tidak mengandalkan tebakan tipe pandas.
  - Nominal Rupiah disimpan sebagai bilangan bulat rupiah, bukan desimal/float.
  - Sel kosong = **tidak tersedia**; `0` = **nilai nol**. Saat membaca, matikan konversi NA default pandas
    selain sel kosong, dan jangan pernah mengisi kosong dengan 0. Kondisi "terlambat diperbarui" dicatat
    di metadata sumber (tanggal snapshot), bukan di sel data.
- LangGraph untuk orkestrasi AI agent — setelah fondasi siap.