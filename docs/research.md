# Riset Data dan Sumber

## Ringkasan keputusan

Baseline kajian adalah DBH SDA Perikanan **TA 2026**, dengan pemantauan nasional berjalan. Perluasan ke agregat `Se-Prov` TA2026 menunggu verifikasi data tiap wilayah. `Se-Prov` adalah agregat wilayah provinsi beserta kabupaten/kotanya, bukan otomatis entitlement pemerintah provinsi.

Angka SIKD yang dibaca di halaman publik adalah tampilan yang dapat dibulatkan dan berubah menurut snapshot. Sumber itu belum cukup untuk merekonstruksi formula alokasi. Karena itu angka yang ada mendukung demonstrator EWS/DSS pemantauan, bukan simulasi alokasi hukum. TA2026 masih berjalan; baseline yang telah diverifikasi saat ini hanya observasi nasional, belum seluruh provinsi.

## Dataset awal yang sudah diperiksa

| Wilayah | Tahun | Pagu | Realisasi | Rasio | Catatan |
|---|---:|---:|---:|---:|---|
| Nasional | 2026 | Rp225,90 M | Rp183,47 M | 81,22% | Snapshot SIKD 22 Oktober 2026; tahun berjalan, angka tampilan bukan nominal exact. |
| Nasional | 2025 | Rp714,66 M | Rp714,66 M | 100,00% | Historis; snapshot yang diperiksa 21 Oktober 2026. |
| Agregat `Se-Prov` Kepulauan Riau | 2025 | Rp25,38 M | Rp25,38 M | 100,00% | Historis; snapshot 17 Oktober 2026; bukan alokasi khusus Pemprov Kepri. |
| Agregat `Se-Prov` Riau | 2025 | Rp14,79 M | Rp14,79 M | 100,00% | Historis; snapshot 9 Oktober 2026; bukan alokasi khusus Pemprov Riau. |

**Pemeriksaan angka acuan baseline:** rasio nasional TA2026 dari angka tampilan adalah `183,47 / 225,90 × 100 = 81,22%`; gap tampilan Rp42,43 M. Ini hanya mereproduksi hitungan dari angka yang telah dibulatkan SIKD, sehingga tidak memvalidasi nominal rupiah exact atau formula alokasi. Data 2026 adalah snapshot tahun berjalan, bukan angka final tahunan.

TA2025 menjadi periode historis/pembanding jika definisi, tingkat wilayah, dan snapshot dapat disejajarkan. Data per provinsi TA2025 tidak boleh dicampur dalam ringkasan baseline TA2026.

## Sumber publik dan kegunaannya

1. **SIKD DJPK, nasional TA 2026** — [Portal data TKD](https://djpk.kemenkeu.go.id/portal/data/tkdd?provinsi=--&tahun=2026). Snapshot 22 Oktober 2026 menampilkan pagu DBH SDA Perikanan 225,90 M, realisasi 183,47 M, dan rasio 81,22%; TA2026 masih berjalan.
2. **SIKD DJPK, nasional TA 2025 (historis)** — [Portal data TKD](https://djpk.kemenkeu.go.id/portal/data/tkdd?provinsi=--&tahun=2025). Snapshot 21 Oktober 2026 menampilkan pagu dan realisasi 714,66 M.
3. **SIKD DJPK, agregat Kepri dan Riau TA2025 (historis)** — [Kepri](https://djpk.kemenkeu.go.id/portal/data/tkdd?provinsi=31&tahun=2025) dan [Riau](https://djpk.kemenkeu.go.id/portal/data/tkdd?pemda=--&provinsi=04&tahun=2025). Contoh historis dengan snapshot berbeda, bukan baseline 2026.
4. **PP 37/2023** — [Dokumen BPK](https://peraturan.bpk.go.id/Download/313156/PP%20Nomor%2037%20Tahun%202023.pdf). Kerangka pengelolaan transfer ke daerah; penerapan untuk proses 2026 perlu dipasangkan dengan aturan pelaksanaan yang berlaku.
5. **PMK 35/2026** — [JDIH Kementerian Keuangan](https://jdih.kemenkeu.go.id/dok/pmk-35-tahun-2026). Rujukan pengelolaan DBH/DAU yang harus diperiksa pasal, ketentuan berlaku, dan transisinya untuk proses yang dimodelkan.
6. **Perpres 201/2024 dan KMK 29/2025** — rincian/penyesuaian TA2025, dipakai sebagai sumber historis bila diperlukan, bukan pagu baseline TA2026.
7. **Materi KLC DJPK: Kebijakan DBH SDA** — [Halaman KLC](https://klc2.kemenkeu.go.id/kms/knowledge/kebijakan-dana-bagi-hasil-sumber-daya-alam-0a2d89ef/detail/). Bahan orientasi; klaim operasional tetap harus dilacak ke regulasi primer dan dataset.

## Ketersediaan dan batas data

- Baseline TA2026 saat ini berisi snapshot nasional per 22 Oktober 2026. Data 38 agregat `Se-Prov` TA2026 belum diverifikasi/dimasukkan.
- Data TA2025 yang tersimpan adalah historis; jangan gabungkan dengan angka TA2026. Jika dipakai untuk tren, samakan level wilayah dan definisi.
- Jangan menjumlahkan angka nasional dengan agregat provinsi atau kabupaten/kota karena tingkatnya tumpang tindih.
- SIKD yang diperiksa menyajikan postur tahunan pagu/realisasi; bukti ini tidak cukup untuk mengeluarkan sinyal keterlambatan penyaluran sepanjang tahun.
- Antarmuka yang diperiksa belum membuktikan API atau ekspor machine-readable. Gunakan fixture berprovenance sampai cara ekspor dan izin pemakaian diverifikasi.
- Untuk menghitung ulang alokasi perlu data tingkat penerima kabupaten/kota secara nasional, basis penerimaan/PNBP, luas laut, indikator kinerja yang memang dipersyaratkan, aturan tahun/proses terkait, serta contoh perhitungan yang dapat direproduksi. Agregat `Se-Prov` tidak memadai.
- BPS/KKP dan dokumen PPID daerah berguna untuk konteks atau rekonsiliasi, tetapi definisi, periode, dan basis harus cocok sebelum digabungkan.

## Daftar verifikasi terbuka

| ID | Pertanyaan | Status | Dampak |
|---|---|---|---|
| SRC-01 | Dapatkah seluruh 38 agregat `Se-Prov` TA2026 diekstrak pada tanggal snapshot yang sama? | Belum dilakukan; baru nasional tersedia pada baseline | Blocker perbandingan lintas provinsi yang konsisten. |
| SRC-02 | Apakah portal menyediakan nominal mentah, ekspor, atau bukti penyaluran per periode? | Belum terverifikasi | Tanpa itu, hasil hanya pada presisi tampilan tahunan. |
| SRC-03 | Apa pagu dan perubahan resmi TA2026, dan bagaimana rekonsiliasinya dengan SIKD? | Perlu ekstraksi sumber APBN/penyesuaian TA2026 | Jangan gunakan pagu historis 2025 sebagai baseline berjalan. |
| SRC-04 | Apa rincian data formula DBH Perikanan untuk seluruh penerima dan tahun/proses 2026? | Kerangka hukum ditemukan; aturan pelaksanaan, input, dan golden case TA2026 belum lengkap | Blocker untuk estimasi alokasi per daerah. |
| SRC-05 | Bagaimana tanggal pembaruan SIKD dan koreksi historis bekerja? | Belum terverifikasi | Fixture wajib menyimpan `source_as_of` dan `retrieved_at`. |
| SRC-06 | Apakah angka SIKD cocok dengan dokumen audited daerah pada basis dan versi yang sama? | Perlu rekonsiliasi terpilih | Catat selisih dan beda definisi; jangan menganggap angka dashboard sebagai audit. |
| GOV-01 | Apakah Cetak Biru SIKD 2025–2029 pada diagram benar bernomor KEP-65/PK/2025? | Belum terverifikasi | Jangan jadikan klaim keselarasan sebagai fakta sebelum sumber primer diperoleh. |

## Catatan substansi formula

PP 37/2023 memberi kerangka pembagian DBH SDA Perikanan, termasuk komponen pembagian 60% merata dan 40% berdasar luas laut. Struktur pada diagram yang diberikan juga menunjukkan komponen alokasi 90% formula dan 10% kinerja. Untuk baseline 2026, verifikasi aturan operasional dan ketentuan transisi yang berlaku, daftar penerima, nilai input resmi, metode indikator, pembulatan, serta angka acuan TA2026. Jangan menerapkan aturan 2026 secara retroaktif pada observasi historis 2025 dan jangan menggunakan formula Minerba untuk Perikanan.

Setiap rekaman sumber harus membawa URL, instansi, jenis dokumen, tahun, tingkat wilayah, tanggal snapshot, tanggal pengambilan, unit, angka persis seperti ditampilkan, presisi, status verifikasi, dan catatan rekonsiliasi. `0`, `NOT_AVAILABLE`, dan `NOT_VERIFIED` memiliki arti berbeda.
