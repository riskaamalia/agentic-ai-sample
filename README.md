# EWS DBH SDA Perikanan

Rancangan vertical slice untuk prototype Early Warning System (EWS) dan Decision Support System (DSS) DBH SDA Perikanan. Fokus awal: TA 2024, data publik DJPK/SIKD, engine deterministik, UI Streamlit, dan perbandingan baseline dengan asumsi skenario.

**Status:** UI prototype awal dan fungsi hitung deterministik sudah ditulis di `src/`. Dependensi perlu dipasang untuk menjalankan UI. Prototype belum direview ML/BA; Definition of Done card belum terpenuhi.

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

Engine Python menghitung rasio, gap, dan perubahan skenario secara deterministik. UI memakai Streamlit. Setiap hasil menampilkan sumber, waktu snapshot, satuan, presisi, dan batasannya. Data tahunan tidak digunakan untuk menyimpulkan keterlambatan penyaluran. Formula alokasi Minerba dari materi diagram tidak diterapkan pada Perikanan.

## Menjalankan UI prototype

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
streamlit run src/app.py
```

UI berisi baseline nasional dan contoh daerah dari fixture, input pagu/realisasi alternatif, metrik skenario, delta terhadap baseline, serta tautan sumber. Provinsi Jawa Barat ditampilkan sebagai belum terverifikasi.

## Langkah kerja berikutnya

Jalankan UI di lingkungan dengan Streamlit, tinjau hasil bersama ML/BA, perbaiki blocker, lalu verifikasi nominal dan snapshot sumber sebelum memperluas cakupan. Ikuti quality gate dan catat review manusia; jangan menganggap AI sebagai reviewer internal.
