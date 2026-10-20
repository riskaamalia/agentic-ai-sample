# Riset Data dan Sumber

## Ringkasan keputusan

Prototype memakai **DBH SDA Perikanan TA 2024** sebagai vertical slice. Sumber primer yang paling mudah dibandingkan antarwilayah adalah Portal Data SIKD DJPK, yang menampilkan akun, anggaran/pagu, realisasi, persentase, filter tahun, wilayah, dan subwilayah. Untuk versi demo, gunakan satu snapshot yang tanggal pengambilannya dicatat. Tampilan portal membulatkan beberapa angka ke dua desimal dalam satuan miliar rupiah; angka tampilan tidak boleh diperlakukan sebagai nilai rupiah exact.

Prototype ini memantau dan membandingkan nilai pagu serta realisasi yang dipublikasikan. Prototype **tidak menghitung ulang formula alokasi hukum**. Diagram yang dibahas sebelumnya memuat formula Minerba, sehingga bobot, data dasar, atau aturan Minerba tidak ditransfer ke Perikanan.

## Dataset awal yang dapat diperiksa

| Wilayah | Tahun | Pagu | Realisasi | Persentase di sumber | Catatan |
|---|---:|---:|---:|---:|---|
| Nasional | 2024 | Rp951,70 miliar | Rp944,29 miliar | 99,22% | Snapshot SIKD; ditampilkan sebagai agregat nasional. |
| Kota Bandung | 2024 | Rp1,07 miliar | Rp1,07 miliar | 100,00% | Snapshot SIKD; angka dua desimal miliar. |
| Kab. Sumedang | 2024 | Rp1,10 miliar | Rp1,10 miliar | 100,00% | Snapshot SIKD; LKPD audited Sumedang juga memuat nilai rinci, perlu dicocokkan sebelum dijadikan acceptance fixture. |
| Kab. Bandung Barat | 2024 | Rp1,07 miliar | Rp1,07 miliar | 100,00% | Snapshot SIKD; angka dua desimal miliar. |
| Provinsi Jawa Barat | 2024 | Belum dimasukkan | Belum dimasukkan | — | PPID Jabar menyediakan LKPD/LRA 2024 audited, tetapi nilai akun Perikanan harus diekstrak dan dicocokkan dengan filter wilayah SIKD. Jangan isi nol saat belum ditemukan. |

**Kecocokan awal AC-03:** perhitungan dari angka agregat nasional yang tampil di SIKD adalah `(944,29 / 951,70) × 100 = 99,2216…%`, dibulatkan dua desimal menjadi **99,22%**, sama dengan tampilan sumber. Bukti ini cocok untuk memeriksa aturan pembulatan terhadap angka tampilan, tetapi belum membuktikan perhitungan dari nominal rupiah tanpa pembulatan. Untuk acceptance final, ambil nominal dasar yang lebih presisi atau dokumentasikan keterbatasan presisinya.

## Sumber publik

1. **Portal Data SIKD DJPK, nasional 2024** — https://djpk.kemenkeu.go.id/portal/data/tkdd?pemda=--&provinsi=--&tahun=2024. Menampilkan DBH SDA Perikanan nasional: pagu Rp951,70 miliar, realisasi Rp944,29 miliar, 99,22%. Keterangan sumber menyebut data SIKD fitur Lacak Salur (CakLur). Snapshot halaman yang diperiksa bertanggal 19 Oktober 2026.
2. **Portal Data SIKD DJPK, Kota Bandung 2024** — https://djpk.kemenkeu.go.id/portal/data/tkdd?pemda=17&provinsi=10&tahun=2024. Menampilkan pagu/realisasi DBH SDA Perikanan Rp1,07 miliar / Rp1,07 miliar (100%). Snapshot halaman yang diperiksa bertanggal 18 Oktober 2026.
3. **Portal Data SIKD DJPK, Kab. Sumedang 2024** — https://djpk.kemenkeu.go.id/portal/data/tkdd?pemda=15&provinsi=10&tahun=2024. Menampilkan Rp1,10 miliar / Rp1,10 miliar (100%). Snapshot halaman yang diperiksa bertanggal 19 Oktober 2026.
4. **Portal Data SIKD DJPK, Kab. Bandung Barat 2024** — https://djpk.kemenkeu.go.id/portal/data/tkdd?pemda=26&provinsi=10&tahun=2024. Menampilkan Rp1,07 miliar / Rp1,07 miliar (100%). Snapshot halaman yang diperiksa bertanggal 18 Oktober 2026.
5. **PPID Pemprov Jawa Barat, daftar informasi berkala** — https://ppid.jabarprov.go.id/pages/info-berkala. Daftar tersebut memuat LRA Pemprov Jabar TA 2024, CaLK 2024, serta dokumen anggaran. Gunakan untuk menelusuri nominal tingkat provinsi; daftar dokumen saja belum menjadi bukti nominal DBH SDA Perikanan.
6. **LKPD Pemprov Jawa Barat TA 2024 audited (CaLK)** — https://file.jabarprov.go.id/live/media/docs/archives/1749801566-25.-Informasi-CaLK-Pemerintah-Daerah-tahun-2024.pdf. Ringkasan mencatat pendapatan transfer dan pendapatan DBH SDA agregat. Nilai akun Perikanan dan kesesuaiannya dengan definisi data SIKD masih harus dikonfirmasi dari tabel rinci.
7. **LKPD Kab. Sumedang TA 2024 audited** — https://fliphtml5.com/szrpa/cfue/. Salinan publik yang ditemukan menampilkan DBH SDA Perikanan anggaran/realisasi 2024 Rp1.097.155.000 dan realisasi 2023 Rp1.444.887.211. Cari/arsipkan salinan resmi PPID/BKAD sebelum menyebut tautan salinan ini sebagai sumber primer acceptance.
8. **Peraturan Bupati Bandung No. 247 Tahun 2024, JDIH Kabupaten Bandung** — https://jdih.bandungkab.go.id/asset/file_hukum/No_247_Tahun_2024__677b940ae0d803.06129408.pdf. Tabel perubahan/penjabaran anggaran menampilkan DBH SDA Perikanan Rp833.805.000. Ini adalah data dokumen anggaran, bukan realisasi audited.
9. **PMK 67 Tahun 2024, JDIH Kementerian Keuangan** — https://jdih.kemenkeu.go.id/dok/pmk-67-tahun-2024. Peraturan tersebut mengatur pengelolaan DBH dan DAU pada periodenya, tetapi halaman JDIH mencatat telah dicabut oleh PMK 35 Tahun 2026 pada 25 Mei 2026. Untuk interpretasi TA 2024, catat aturan yang berlaku pada tanggal dan proses terkait; jangan memakai PMK 35/2026 secara retroaktif sebagai mesin hitung TA 2024 tanpa tinjauan kebijakan.
10. **Materi KLC DJPK: Kebijakan Dana Bagi Hasil Sumber Daya Alam** — https://klc2.kemenkeu.go.id/kms/knowledge/kebijakan-dana-bagi-hasil-sumber-daya-alam-0a2d89ef/detail/. Materi publik terbit 20 Mei 2025. Gunakan sebagai bahan orientasi; halaman tidak menyediakan transkrip yang dapat diperiksa, sehingga klaim operasional harus dilacak ke regulasi/data primer.

## Ketersediaan, granularitas, dan pembaruan

- SIKD menyediakan tampilan agregat nasional serta filter wilayah/subwilayah. Granularitas yang terlihat pada halaman adalah tahunan dan per akun/wilayah, bukan seri penyaluran bulanan pada detail hasil yang dibaca.
- Keterangan halaman memakai snapshot CakLur dengan tanggal berbeda per halaman (18–19 Oktober 2026). Angka historis dapat berubah ketika data diperbarui atau direkonsiliasi; simpan tanggal akses dan versi snapshot.
- Antarmuka publik yang diperiksa tidak membuktikan adanya API atau ekspor machine-readable. Jangan membangun integrasi API sebelum endpoint/izin/format diverifikasi. Vertical slice boleh menggunakan fixture CSV yang disalin dan diberi sumber, waktu ekstraksi, serta status pembulatan.
- LKPD/DPA/Perda daerah biasanya berupa dokumen tahunan, sementara SIKD menyajikan postur penyaluran. Angka antarjenis dokumen dapat berbeda karena basis, versi anggaran, tanggal snapshot, serta definisi anggaran/realisasi. Jangan gabungkan sebelum direkonsiliasi.

## Daftar verifikasi terbuka

| ID | Pertanyaan | Status | Dampak |
|---|---|---|---|
| SRC-01 | Berapa nominal DBH SDA Perikanan TA 2024 untuk entitas Provinsi Jawa Barat sendiri, dan apakah tercatat sebagai penerima pada sumber yang sama? | Belum terverifikasi | Jangan render sebagai nol; tampilkan `belum terverifikasi` sampai data resmi cocok. |
| SRC-02 | Dapatkah SIKD menyediakan nominal mentah, file ekspor, atau bukti penyaluran per periode? | Belum terverifikasi | Perbandingan hanya pada presisi tampilan tahunan; jangan klaim peringatan keterlambatan berkala. |
| SRC-03 | Apakah angka SIKD untuk Sumedang, Bandung, dan Bandung Barat cocok dengan LKPD audited/dokumen anggaran TA 2024 pada basis yang sama? | Perlu rekonsiliasi | Catat selisih dan beda definisi; SIKD menjadi fixture demonstrasi, bukan otomatis angka audit. |
| SRC-04 | Dokumen/regulasi mana yang menetapkan pembagian penerimaan DBH Perikanan yang relevan untuk TA 2024? | Tinjauan kebijakan | Tanpa sumber tersebut engine tidak menghitung ulang formula alokasi. |
| SRC-05 | Bagaimana tanggal pembaruan SIKD dan kebijakan koreksi historis bekerja? | Belum terverifikasi | Semua fixture wajib menyimpan `source_as_of` dan `retrieved_at`. |

## Aturan pencatatan data sumber

Setiap rekaman membawa URL sumber, judul/instansi, jenis dokumen, tahun anggaran, tanggal snapshot, tanggal pengambilan, satuan asli, nominal asli jika tersedia, angka yang ditampilkan, presisi, status verifikasi, dan catatan rekonsiliasi. `0`, `null`, `not_available`, dan `not_verified` memiliki makna terpisah.
