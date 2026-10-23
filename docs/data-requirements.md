# Daftar Kebutuhan Data — Simulator DBH Perikanan, EWS, dan DSS

## 1. Tujuan dokumen

Dokumen ini menerjemahkan empat diagram kebutuhan yang dibagikan ke inventaris data untuk:

1. asesmen kondisi eksisting dan gap analysis SIKD;
2. definisi ruang lingkup serta kapabilitas target SIKD Cerdas;
3. rancangan DSS/EWS dan arsitektur bisnis, data, aplikasi, teknologi, analitik, integrasi, interoperabilitas, dan tata kelola;
4. use case simulator DBH SDA Perikanan: input → validasi/proses → output keputusan dan perbandingan skenario.

**Batas penting:** daftar ini mendeskripsikan data yang dibutuhkan, bukan menyatakan seluruh data sudah tersedia atau formula sudah disahkan. Data produksi perikanan, data keuangan daerah, dan pagu/realisasi SIKD tidak boleh diasumsikan sebagai variabel formula alokasi sebelum kecocokannya dibuktikan pada regulasi yang berlaku untuk tahun/proses tersebut. Formula Minerba pada salah satu diagram tidak digunakan untuk DBH Perikanan.

## 2. Ringkasan: apa yang perlu dikumpulkan

| Kelompok | Kegunaan | Prioritas MVP | Pemilik/sumber yang disarankan |
|---|---|---:|---|
| Dasar hukum dan parameter formula | Menetapkan variabel, bobot, kategori daerah, versi formula, dan pembulatan | P0 — blocker | DJPK/Kemenkeu; JDIH; reviewer hukum/domain |
| Penerimaan DBH Perikanan dan data dasar asersi | Menjadi basis penghitungan sesuai aturan; perlu status awal/final/revisi | P0 — blocker | DJPK, KKP, unit pemilik PNBP/perikanan |
| Daerah penerima dan klasifikasi | Memetakan provinsi/kabupaten/kota dan kategori yang ditetapkan | P0 — blocker | DJPK dan KKP; keputusan/daftar penetapan resmi |
| Pagu/alokasi resmi dan pembaruan | Pembanding hasil simulasi dan rekonsiliasi | P0 | Perpres rincian APBN/perubahannya; DJPK/SIKD |
| Variabel kinerja yang diwajibkan aturan | Menghitung komponen formula hanya jika memang berlaku untuk Perikanan | P0 jika diwajibkan aturan | KKP/KL teknis; DJPK; berita acara verifikasi |
| Data historis dan realisasi | Perbandingan antarperiode dan konteks EWS | P1 | SIKD, LKPD/LRA, sumber sektoral |
| Jejak proses, kualitas, dan review | Audit trail, alert data, tindak lanjut ML/BA | P0 | Log sistem/proses dan catatan internal pemilik data |
| Inventaris sistem/proses eksisting | Asesmen gap dan rancangan model target | P1 untuk deliverable desain | Pemilik SIKD, unit bisnis, TI, keamanan, data governance |

**P0** berarti diperlukan sebelum engine mengeluarkan simulasi alokasi. **P1** dapat menyusul untuk analisis yang lebih luas dan desain target.

## 3. Data publik yang dapat dipakai atau ditelusuri

| Data / sumber | Isi yang relevan | Penggunaan yang diperbolehkan | Catatan verifikasi |
|---|---|---|---|
| [Portal Data SIKD DJPK — nasional TA 2026](https://djpk.kemenkeu.go.id/portal/data/tkdd?provinsi=--&tahun=2026) | Pagu, realisasi, rasio per jenis TKD | Baseline monitoring nasional berjalan | Snapshot 22 Oktober 2026 menampilkan DBH SDA Perikanan 225,90 M / 183,47 M (81,22%). Angka tampilan dibulatkan; tahun belum selesai. |
| [Portal Data SIKD DJPK — nasional TA 2025](https://djpk.kemenkeu.go.id/portal/data/tkdd?provinsi=--&tahun=2025) | Pagu/anggaran, realisasi, persentase menurut jenis TKD | Pembanding historis | Snapshot yang diperiksa 21 Oktober 2026 menampilkan DBH SDA Perikanan 714,66 M untuk pagu dan realisasi. Angka tampilan bukan nominal exact. |
| [Portal Data SIKD DJPK — agregat Provinsi Kepulauan Riau TA 2025](https://djpk.kemenkeu.go.id/portal/data/tkdd?provinsi=31&tahun=2025) dan [agregat Provinsi Riau TA 2025](https://djpk.kemenkeu.go.id/portal/data/tkdd?provinsi=04&tahun=2025) | Contoh pagu/realisasi `Se-Prov` | Uji struktur agregat provinsi dan format sumber | Snapshot halaman tidak serentak (contoh Kepri 17 Okt dan Riau 9 Okt 2026). Kumpulkan ulang semua provinsi pada tanggal yang sama. `Se-Prov` adalah agregat wilayah, jangan otomatis disebut alokasi pemerintah provinsi. |
| [PPID pemerintah daerah — katalog dokumen APBD/LRA/CaLK](https://ppid.jabarprov.go.id/pages/info-berkala) | Contoh katalog dokumen Pemprov Jawa Barat; tiap daerah memiliki PPID masing-masing | Rekonsiliasi untuk wilayah yang dipilih dan jika sumber pusat/daerah perlu dicocokkan | Untuk cakupan seluruh Indonesia katalog PPID Jabar hanya contoh. Buka laporan TA 2025 yang tepat untuk setiap daerah; periksa audited status, akun, basis, dan tabel. |
| [BPS Jawa Barat — produksi/nilai tangkap kabupaten/kota 2024](https://jabar.bps.go.id/id/statistics-table/3/U2k4d1MwcFZjRGhSVVRKaWRHRm5Temw1VURJeFp6MDkjMw%3D%3D/volume-produksi-dan-nilai-produksi-perikanan-tangkap-menurut-kabupaten-kota-dan-jenis-penangkapan-di-provinsi-jawa-barat--2024.html) | Statistik sektoral tahun 2024 sebagai tahun historis terakhir yang teridentifikasi dalam riset ini | Konteks dan pemeriksaan kewajaran; bukan baseline TKD 2025 | Bukan otomatis data dasar DBH. BPS memberi makna khusus pada `-`, `NA`, estimasi, revisi, dan penjumlahan. Cari seri 2025 setelah terbit dan jangan samakan simbol dengan nol. |
| [BPS — produksi perikanan tangkap menurut provinsi, 2024](https://www.bps.go.id/id/statistics-table/2/MTUwNiMy/produksi-) | Pembanding statistik provinsi/nasional historis | Konteks sektoral saja | Tidak menggantikan data daerah penerima, PNBP, atau tahun data formula. |
| [KKP — laporan kinerja DJPT 2024](https://ppid.kkp.go.id/media/uploads/document_information_public/LKJ_DJPT_TAHUN_2024.pdf) | Statistik dan capaian sektor perikanan tangkap | Konteks dan definisi indikator | Periksa beda tahun rilis dengan tahun observasi; bukan data alokasi TKD. |
| [KKP — informasi PNBP Perikanan dan alokasi APBN 2025](https://ppid.kkp.go.id/upp/direktorat-jenderal-perikanan-tangkap/news/detail/kkp-perkuat-pembangunan-fasilitas-perikanan-tangkap-di-indonesia-timur/) | Publikasi agregat PNBP SDA Perikanan 2024 dan jumlah yang dialokasikan pada APBN 2025 | Cross-check tingkat nasional | Publikasi ini tidak memberikan rincian seluruh input formula per daerah; jangan menganggap angka agregat cukup untuk menghitung pagu tiap provinsi/kabupaten. |
| [PMK 67 Tahun 2024 — JDIH Kemenkeu](https://jdih.kemenkeu.go.id/dok/pmk-67-tahun-2024) | Kerangka pengelolaan DBH dan DAU pada masa berlakunya | Referensi historis untuk proses yang berlaku pada 2025 | Dicabut pada 2026; jangan gunakan sebagai aturan baseline proses TA2026 tanpa memeriksa status dan transisi. |
| [PMK 35 Tahun 2026 — JDIH Kemenkeu](https://jdih.kemenkeu.go.id/dok/pmk-35-tahun-2026/summary) | Kerangka pengelolaan DBH/DAU tahun berjalan, termasuk data dasar, verifikasi, perhitungan, kinerja, dan settlement | Rujukan utama yang perlu diperiksa untuk proses TA2026 | Pastikan pasal dan ketentuan berlaku/transisi untuk tahap proses yang dimodelkan; jangan menyimpulkan semua data sudah tersedia. |
| [Perpres 201 Tahun 2024 — rincian APBN 2025](https://jdih.kemenkeu.go.id/dok/perpres-201-tahun-2024) dan [KMK 29 Tahun 2025 — penyesuaian rincian alokasi TKD](https://jdih.kemenkeu.go.id/dok/kmk-29-tahun-2025/files) | Rincian alokasi TA 2025 dan penyesuaian dalam tahun anggaran | Pembanding resmi untuk memeriksa angka per daerah/versi alokasi | Bedakan pagu Perpres awal, penyesuaian KMK, dan tampilan realisasi/pagu SIKD. Catat versi yang dibandingkan. |
| [PMK 120 Tahun 2025 — penetapan kurang bayar/lebih bayar DBH](https://jdih.kemenkeu.go.id/dok/pmk-120-tahun-2025/summary) | Rincian KB/LB sampai TA 2024 menurut jenis DBH dan daerah | Konteks rekonsiliasi historis | Bukan pagu DBH Perikanan TA 2025; jangan dicampur dengan alokasi berjalan. |

### Cara memakai data statistik perikanan

Statistik produksi/nilai perikanan BPS/KKP berguna untuk konteks industri dan pengecekan data, tetapi tidak membuktikan sendiri daerah penerima DBH atau besaran hak alokasi. Pakai sebagai faktor formula hanya jika aturan DBH Perikanan yang berlaku secara eksplisit menyebut indikator tersebut, tahun dasar, cakupan, metode, dan sumber datanya.

### Cakupan Jawa Barat

Baseline dashboard adalah nasional TA2026; target perluasan adalah agregat `Se-Prov` TA2026 pada 38 provinsi dengan snapshot yang dicatat. Saat ini fixture hanya memiliki observasi nasional 2026. Jangan menjumlahkan nasional, agregat `Se-Prov`, dan kabupaten/kota karena tingkat tersebut tumpang tindih. Untuk mereproduksi formula alokasi, perlu daftar seluruh penerima kabupaten/kota nasional; agregat provinsi tidak memadai. Jika sumber tidak memuat observasi, simpan sebagai `NOT_AVAILABLE` atau `NOT_VERIFIED`, bukan nol.

## 4. Data internal/terbatas yang perlu diminta dari pemilik data

Data berikut mungkin tidak seluruhnya tersedia terbuka. Minta hanya field yang diperlukan, definisi, pemilik data, izin penggunaan, level klasifikasi, dan cara penyimpanannya. Jangan menaruh data terbatas/rahasia ke repo demo publik.

| Data internal | Field minimum yang diminta | Pemilik data yang disarankan | Kegunaan |
|---|---|---|---|
| Data dasar DBH Perikanan tervalidasi | Jenis penerimaan/PNBP, tahun/periode, nilai asersi, nilai final/revisi, kode akun, unit, waktu pencatatan, status verifikasi | DJPK dan unit KKP pemilik data penerimaan | Menetapkan basis input yang sah untuk kalkulasi. |
| Berita acara konfirmasi/rekonsiliasi | Pihak yang mengonfirmasi, tanggal, periode, nilai yang disepakati, perbedaan, keputusan, nomor dokumen, status final | DJPK, KKP, unit Kemenkeu terkait | Menjelaskan mana angka yang telah disetujui dan menyelesaikan selisih antarinstansi. |
| Penetapan daerah penghasil/penerima dan kategori | Kode wilayah, nama, level, kategori menurut regulasi, dasar penetapan, tanggal berlaku, status perubahan | DJPK/KKP dan instansi penetap | Memetakan alokasi kepada entitas yang benar untuk periode perhitungan. |
| Data indikator/kinerja yang diwajibkan formula | Nama indikator persis sesuai aturan, nilai, metode, unit, tahun dasar, pemilik, sumber, status verifikasi, aturan fallback | KKP/KL teknis dan DJPK | Menghitung komponen kinerja hanya bila dipersyaratkan untuk DBH Perikanan. Jangan mengasumsikan indikator lingkungan atau bobot dari Minerba berlaku. |
| Parameter formula resmi | Formula ID/version, pasal/lampiran, tanggal berlaku, variabel, bobot/koefisien, pembulatan, aturan residual, kasus fallback, persetujuan reviewer | DJPK/legal reviewer | Mengunci kalkulasi deterministik, audit trail, dan perubahan kebijakan. |
| Workbook/hasil kalkulasi acuan | Input snapshot, langkah hitung, alokasi per daerah, total, pagu, versi workbook, tanggal, pemilik, status disetujui | Tim analis/pengolah alokasi DJPK | Golden case untuk membandingkan output engine dan memenuhi traceability. |
| Rincian pagu dan perubahannya | Pagu awal, revisi, pagu final, daerah, jenis DBH, dasar keputusan, tanggal berlaku, satuan | DJPK dan pengelola APBN/TKD | Rekonsiliasi hasil skenario dan perbandingan versi pagu. |
| Snapshot penyaluran/monitoring yang lebih rinci | Periode, tanggal update, nilai salur, koreksi, status transaksi, definisi status, kode wilayah dan akun | DJPK/SIKD atau unit penyalur | Sinyal EWS perkembangan data/penyaluran; dipakai hanya jika frekuensi dan jadwal pembaruan diketahui. |
| Dokumen keuangan daerah yang dapat dicocokkan | LRA audited, CaLK, kode akun, anggaran/realisasi, periode, halaman/tabel, koreksi | BPKAD/PPID provinsi dan kabupaten/kota | Rekonsiliasi observasi SIKD dengan laporan daerah; tidak menggantikan basis pusat tanpa penyamaan definisi. |
| Inventaris proses dan sistem eksisting | Nama aplikasi, pemilik, proses, input/output, jadwal, integrasi, format, volume, SLA, masalah yang diketahui | Business owner SIKD, DJPK, unit TI | Asesmen kondisi eksisting dan gap analysis pada Deliverable 1. |
| Kamus data dan tata kelola | Definisi field, kode referensi, wali data, sumber otoritatif, lineage, klasifikasi, retensi, hak akses, prosedur koreksi | Data owner/steward, keamanan informasi | Menentukan interoperabilitas, kualitas, akses, audit, dan perubahan data. |
| Kebutuhan pengguna dan keputusan yang didukung | Peran pengguna, pertanyaan keputusan, tindakan setelah alert, ambang yang disetujui, eskalasi, batas wewenang | Analis fiskal, reviewer ML/BA, pemilik proses | Menentukan output EWS/DSS dan menghindari alert yang tidak punya tindakan atau dasar. |
| Log review/issue dan keputusan | Versi artefak, reviewer/role, tanggal, temuan, keputusan, issue ID, owner, due date, status | Tim proyek dan reviewer | Bukti Quality Gate dan tindak lanjut blocker showcase. |

## 5. Data minimum per komponen diagram

### A. Input data

- Penerimaan/basis DBH Perikanan dengan nilai dan status validasi.
- Tahun anggaran, periode data, jenis DBH, akun, sumber, dan versi dokumen.
- Daftar wilayah beserta kode, level pemerintahan, kategori penerima, dan dasar penetapannya.
- Variabel serta bobot formula dari regulasi yang tepat; jika belum terverifikasi, variabel hanya dicatat sebagai kandidat dan tidak dihitung.
- Data historis yang diperlukan formula atau analisis tren, dengan periode, definisi, dan sumber konsisten.
- Pagu indikatif, pagu awal/perubahan/final, dan tahun acuan yang dapat direkonsiliasi.
- Provenance lengkap: institusi, judul, URL/dokumen/nomor halaman, tanggal snapshot, tanggal ekstraksi, satuan, presisi, metode transkripsi, status verifikasi, dan catatan perubahan.

### B. Validasi dan mesin simulasi

- Kelengkapan field serta keterkaitan satuan/periode/level wilayah.
- Pemeriksaan duplikasi kode wilayah, agregasi yang tumpang tindih, nilai hilang, nol, nilai dibulatkan, serta revisi.
- Formula dan bobot berversi yang hanya bisa dipakai setelah persetujuan domain/legal.
- Perubahan parameter baseline vs skenario dengan alasan dan sumber; nilai sumber asli tidak ditimpa.
- Rekonsiliasi total hasil dengan pagu acuan, dengan residual dan aturan pembulatan tampak.
- Kasus pembanding/acuan independen untuk menghitung ulang setidaknya satu skenario.

### C. Output keputusan, EWS, dan DSS

- Estimasi per wilayah dengan komponen hitung serta versi formula.
- Scenario comparison: nilai baseline, nilai skenario, parameter yang berubah, dampak per wilayah/agregat, serta satuan.
- Selisih antarperiode dan terhadap pagu hanya jika definisi dan basis kedua periode sebanding.
- Jejak audit yang menghubungkan hasil ke input, sumber, asumsi, versi formula, dan waktu proses.
- EWS MVP yang aman: status data tidak lengkap/belum terverifikasi, konflik antar-sumber, pagu/angka yang tidak cocok, atau snapshot usang **hanya jika** jadwal pembaruan resmi tersedia.
- DSS menyajikan bukti, dampak skenario, batasan, dan langkah pemeriksaan; tidak menetapkan kebijakan atau keputusan penyaluran otomatis.

### D. Asesmen dan model target SIKD Cerdas

- Peta proses bisnis saat ini, sistem/aplikasi terkait, aliran pertukaran data, format dan frekuensi.
- Daftar pemilik dan wali data, sumber otoritatif, kontrol kualitas, tata akses, klasifikasi, retensi, dan prosedur koreksi.
- Daftar pengguna dan use case, alert yang dibutuhkan, keputusan yang dibantu, alur review/eskalasi, dan kebutuhan audit.
- Arsitektur aplikasi/teknologi saat ini, integrasi/interoperabilitas, dependensi dan kendala.
- Gap analysis kondisi aktual vs kapabilitas target analitik, EWS, DSS, AI, integrasi, dan governance.
- Dokumen Cetak Biru SIKD yang resmi dan versi berlaku. Materi slide menyebut `KEP-65/PK/2025`, tetapi identitas dokumen tersebut masih perlu diverifikasi sebelum dijadikan acuan kepatuhan.

## 6. Metadata dan kualitas minimum

Setiap variabel mentah maupun turunan sebaiknya membawa:

| Metadata | Contoh / aturan |
|---|---|
| ID data/snapshot | Stabil dan unik untuk pengambilan data tertentu. |
| Definisi dan jenis data | Nama variabel dari sumber, bukan nama yang disimpulkan aplikasi. |
| Periode dan waktu | Tahun/periode berlaku, tanggal snapshot, tanggal ekstraksi, zona waktu jika relevan. |
| Entitas | Kode/nama wilayah dan level; gunakan kode dari rujukan resmi yang disepakati. |
| Nilai dan unit | Simpan nilai sumber tanpa konversi diam-diam; catat unit sumber dan unit kanonis bila dikonversi. |
| Status/presisi | Exact, rounded display, estimated, provisional, revised, not available, zero, not verified. |
| Sumber/lineage | URL, lembaga, nama dokumen, nomor halaman/tabel, metode ekstraksi, transformasi, serta parent input untuk hasil hitung. |
| Formula/version | Formula ID, pasal/lampiran, tanggal berlaku, parameter, aturan pembulatan, kode engine/version. |
| Persetujuan dan batas akses | Pemilik, reviewer, klasifikasi akses, dasar izin penggunaan, catatan rekonsiliasi. |

**Aturan status nilai:** `0` hanya jika sumber menyatakan nol; `NOT_AVAILABLE` jika tidak disajikan; `NOT_VERIFIED` jika masih perlu dicocokkan; `DELAYED` hanya jika frekuensi dan tanggal jatuh tempo update diketahui.

## 7. Rencana pengumpulan bertahap

1. **P0 — Legal dan golden case:** verifikasi pasal/aturan operasional serta formula DBH Perikanan untuk proses dan TA2026, parameter/version, satu workbook/perhitungan acuan, dan berita acara konfirmasi.
2. **P0 — Data alokasi resmi:** temukan rincian pagu APBN dan penyesuaian TA2026; cocokkan rincian per daerah dan versi pagu dengan SIKD.
3. **P0 — Peta daerah dan variabel:** minta penetapan penerima/kategori, kode wilayah, serta indikator yang diwajibkan formula. Simpan sumber dan status verifikasi setiap field.
4. **P1 — Cross-check sektoral/daerah:** ambil BPS/KKP untuk konteks; ambil LRA/CaLK audited dari PPID untuk cocokkan basis; jangan menggabungkan sebelum definisi disejajarkan.
5. **P1 — Asesmen SIKD:** wawancarai pemilik proses/data, dokumentasikan sistem/integrasi, lineage, akses, issue kualitas, kebutuhan pengguna, serta alur tindak lanjut EWS.
6. **Setelah tersedia — Fixture:** versi-kan snapshot kecil dan dokumentasikan lisensi/izin, transformasi, serta hasil review.

Jika data internal tidak dapat diberikan, catat pemilik, permintaan, alasan tidak tersedia, dampak terhadap acceptance criteria, dan opsi perubahan scope. Jangan mengisi gap dengan data sintetis yang tampak seperti nilai resmi.

## 8. Sumber yang diperiksa

- Portal SIKD DJPK TA2026 menampilkan angka nasional; snapshot 22 Oktober 2026 mencatat pagu dan realisasi DBH Perikanan nasional. Data agregat 38 provinsi untuk 2026 masih perlu dikumpulkan dan diverifikasi.
- Portal SIKD DJPK TA2025 dan Perpres 201/2024/KMK 29/2025 menjadi bahan historis, bukan baseline berjalan.
- KKP mempublikasikan angka PNBP nasional, tetapi rincian input formula per daerah belum diverifikasi sebagai data publik terbuka.
- BPS/KKP menyediakan seri sektoral historis yang dapat menjadi konteks; seri tersebut tidak otomatis variabel formula untuk alokasi TA2026.
- PMK 35/2026 perlu diperiksa untuk baseline proses 2026; aturan dan data yang dipakai harus sesuai tanggal/proses yang disimulasikan.
