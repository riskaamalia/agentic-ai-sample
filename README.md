# EWS DBH SDA Perikanan

Rancangan vertical slice DBH SDA Perikanan TA 2026 sebagai use case Early Warning System (EWS) dan Decision Support System (DSS). Baseline awal memakai observasi nasional berjalan dari SIKD; cakupan agregat `Se-Prov` diperluas setelah data tahun 2026 per wilayah berhasil diverifikasi. Target simulator alokasi mencakup input data/parameter, validasi, formula deterministik terverifikasi, estimasi per daerah, scenario comparison, rekonsiliasi pagu, dan jejak hitung.

**Status:** form input Streamlit awal tersedia di `src/app.py`; engine alokasi dan alur runnable end-to-end belum tersedia, dependensi belum terpasang, dan review ML/BA belum dilakukan. Definition of Done card belum terpenuhi.

## Mulai membaca

1. [`docs/clickup-card.md`](docs/clickup-card.md) — scope, DoD, acceptance criteria, evidence.
2. [`docs/research.md`](docs/research.md) — data contoh, sumber, kualitas dan pertanyaan verifikasi.
3. [`docs/data-requirements.md`](docs/data-requirements.md) — inventaris data publik/internal yang diperlukan diagram.
4. [`docs/architecture.md`](docs/architecture.md) — desain komponen.
5. [`docs/data-model.md`](docs/data-model.md) — skema observation, scenario, result, dan review.
6. [`docs/risk-methodology.md`](docs/risk-methodology.md) — rumus dan batas interpretasi sinyal.
7. [`docs/agent-workflow.md`](docs/agent-workflow.md) — alur UI dan review manusia.
8. [`docs/roadmap.md`](docs/roadmap.md) — tahap implementasi.

## Data demonstrasi awal

Snapshot Portal Data SIKD DJPK TA 2026 per 22 Oktober 2026 menampilkan DBH SDA Perikanan nasional dengan pagu Rp225,90 M dan realisasi Rp183,47 M (81,22%). Ini adalah data berjalan dan angka tampilan dibulatkan. Data agregat `Se-Prov` TA2026 belum dimasukkan. Observasi TA2025 tetap disimpan sebagai historis di fixture.

Rincian sumber dan snapshot ada di [`docs/research.md`](docs/research.md). Data portal dapat diperbarui, maka angka di atas adalah contoh sumber, bukan fixture runtime.

## Arsitektur dan batas

Dashboard Streamlit membaca fixture lokal dan dapat membandingkan asumsi sederhana; belum ada pengambilan data otomatis atau perhitungan alokasi. Rasio/gap SIKD dapat menjadi demonstrator monitoring, bukan simulator alokasi yang ditargetkan diagram. Aturan operasional TA2026, data input seluruh penerima, dan angka acuan harus diverifikasi sebelum mengeluarkan estimasi alokasi. Formula Minerba tidak diterapkan pada Perikanan.

## Langkah kerja berikutnya

Verifikasi sumber 2026 per wilayah dan snapshot yang konsisten, tutup blocker dasar hukum/formula serta contoh hitung DBH Perikanan, lalu implementasikan engine deterministik dan UI bertahap. Ikuti quality gate dan catat review manusia; jangan menganggap AI sebagai reviewer internal.
