# EWS DBH SDA Perikanan

Rancangan vertical slice untuk prototype Early Warning System (EWS) dan Decision Support System (DSS) DBH SDA Perikanan. Fokus awal: TA 2024, data publik DJPK/SIKD, engine deterministik, UI Streamlit, dan perbandingan baseline dengan asumsi skenario.

**Status:** tahap dokumentasi rancangan. Belum ada engine atau UI runnable dan belum ada review ML/BA. Jangan menggunakan dokumen ini sebagai klaim bahwa Definition of Done card sudah terpenuhi.

## Mulai membaca

1. [`docs/clickup-card.md`](docs/clickup-card.md) — scope, DoD, acceptance criteria, evidence.
2. [`docs/research.md`](docs/research.md) — data contoh, sumber, kualitas dan pertanyaan verifikasi.
3. [`docs/architecture.md`](docs/architecture.md) — desain komponen.
4. [`docs/data-model.md`](docs/data-model.md) — skema observation, scenario, result, dan review.
5. [`docs/risk-methodology.md`](docs/risk-methodology.md) — rumus dan batas interpretasi sinyal.
6. [`docs/agent-workflow.md`](docs/agent-workflow.md) — alur UI dan review manusia.
7. [`docs/roadmap.md`](docs/roadmap.md) — tahap implementasi.

## Data demonstrasi awal

Portal Data SIKD DJPK untuk TA 2024 menampilkan DBH SDA Perikanan nasional sebesar pagu Rp951,70 miliar dan realisasi Rp944,29 miliar (99,22%). Contoh wilayah Jawa Barat yang ditampilkan SIKD: Kota Bandung Rp1,07 miliar/Rp1,07 miliar; Kab. Sumedang Rp1,10 miliar/Rp1,10 miliar; Kab. Bandung Barat Rp1,07 miliar/Rp1,07 miliar. Angka daerah dibulatkan di tampilan portal. Nilai tingkat Provinsi Jawa Barat masih perlu diverifikasi; data kosong tidak diartikan nol.

Rincian sumber dan snapshot ada di [`docs/research.md`](docs/research.md). Data portal dapat diperbarui, maka angka di atas adalah contoh sumber, bukan fixture runtime.

## Arsitektur dan batas

Engine Python menghitung rasio, gap, dan perubahan skenario secara deterministik. UI MVP direncanakan memakai Streamlit. Setiap hasil perlu menampilkan sumber, waktu snapshot, satuan, presisi, formula versi, dan batasannya. Data tahunan tidak digunakan untuk menyimpulkan keterlambatan penyaluran. Formula alokasi Minerba dari materi diagram tidak diterapkan pada Perikanan.

## Langkah kerja berikutnya

Tutup verifikasi sumber untuk Provinsi Jawa Barat dan nominal daerah yang presisi, lalu implementasikan fixture data sebagai tahap pertama. Ikuti quality gate dan catat review manusia; jangan menganggap AI sebagai reviewer internal.
