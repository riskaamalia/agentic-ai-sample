# Metodologi Sinyal dan Perbandingan Skenario

## Tujuan dan batas interpretasi

Engine MVP memberi **sinyal pemantauan** berdasarkan angka pagu/realisasi dan kualitas datanya. Sinyal bukan temuan penyimpangan, prediksi, keputusan penyaluran, atau penilaian kinerja resmi. Istilah “risiko” harus selalu disertai aturan, data, sumber, periode, dan keterbatasan.

Baseline DBH SDA Perikanan TA2026 yang ditemukan adalah pagu/realisasi nasional pada snapshot berjalan SIKD per 22 Oktober 2026. Data ini bukan angka tutup tahun. Satu snapshot tidak cukup untuk menyimpulkan tren terlambat salur; perlu jadwal penyaluran resmi dan snapshot berkala yang definisinya konsisten.

Diagram kebutuhan menargetkan simulator alokasi. Itu membutuhkan formula resmi, variabel, bobot, basis penerimaan, aturan pengelompokan penerima, serta pagu acuan yang sesuai untuk DBH Perikanan dan tahun terkait. Rujukan formula Minerba pada diagram lain tidak dapat dipindahkan ke Perikanan. Sampai sumber primer dan contoh perhitungan diverifikasi, keluaran alokasi harus berstatus **belum dapat dihitung**. Formula rasio/gap pada dokumen ini hanya untuk pemeriksaan pagu/realisasi SIKD, bukan formula pembagian alokasi.

## Perhitungan deterministik v1

Dengan `B = pagu` dan `R = realisasi`:

1. `rasio_realisasi_pct = R / B × 100`, bila `B > 0` dan kedua nilai tersedia.
2. `sisa_pagu = B - R`, bila kedua nilai tersedia.
3. `selisih_skenario = nilai_skenario - nilai_baseline`.
4. `perubahan_skenario_pct = selisih_skenario / nilai_baseline × 100`, hanya bila baseline tidak nol.

Untuk snapshot nasional TA2026 yang diperiksa: `B = 225,90 M` dan `R = 183,47 M`. Rasio dari angka tampilan adalah **81,22%**, dan gap tampilannya 42,43 M. Karena sumber membulatkan tampilan dan tahun masih berjalan, hasil ini bukan angka final tahunan, nominal exact rupiah, atau validasi formula alokasi.

## Sinyal v1

| Rule ID | Kondisi | Keluaran | Makna |
|---|---|---|---|
| `DQ-001` | Pagu/realisasi hilang atau status belum terverifikasi | `DATA_INCOMPLETE` | Tahan kesimpulan numerik; minta verifikasi sumber. |
| `DQ-002` | Sumber berstatus `ROUNDED_DISPLAY` | `PRECISION_LIMITED` | Boleh hitung demonstrasi pada angka tampilan; hasil bukan nominal presisi penuh. |
| `MON-001` | `R < B` pada snapshot SIKD yang dipilih | `MONITOR_GAP` (advisory) | Ada sisa pagu pada tanggal snapshot; bukan bukti keterlambatan/masalah. Tidak ada ambang risiko bisnis pada rule ini. |
| `MON-002` | `R > B` | `REVIEW_OVER_BUDGET` | Minta reviewer memeriksa beda basis, perubahan pagu, koreksi, atau data. Bukan otomatis kesalahan. |
| `MON-003` | Realisasi dibanding tahun sebelumnya berbeda | `YEAR_OVER_YEAR_CHANGE` | Tampilkan besar perubahan dan label “perlu konteks”; jangan menganggap perubahan sebagai anomali tanpa baseline/ambang yang direview. |

Rule adalah aturan demonstrasi yang harus direview ML/BA. MVP tidak menetapkan threshold persentase materialitas karena belum ada ambang resmi yang disetujui.

## Scenario comparison

Skenario baseline menyalin observation dan menyimpan source/version. Skenario alternatif mengubah satu atau lebih input secara eksplisit dan menyimpan catatan asumsi. UI membandingkan pagu, realisasi, rasio, sisa, serta perubahan terhadap baseline. Contoh baseline nasional: pagu `225,90 M`, realisasi `183,47 M` pada snapshot TA2026; alternatif demo dapat mengubah nilai input. Skenario tersebut tidak boleh dilabeli sebagai realisasi resmi atau ramalan.

Untuk simulator alokasi target, perbandingan harus mengubah parameter yang memang diperbolehkan formula dan membandingkan estimasi tiap wilayah, total hasil, perubahan terhadap baseline, dan residual terhadap pagu acuan. Sebelum aturan perubahan parameter dan contoh perhitungan resmi disetujui, fitur ini belum dapat menghasilkan angka alokasi; skenario rasio/realisasi di atas hanya demonstrator monitoring.

Perbandingan lintas wilayah harus memberi konteks: nilai nominal, pagu relatif, tahun, sumber, tanggal snapshot, tingkat wilayah, dan presisi. Tandai baris SIKD berfilter provinsi sebagai agregat `Se-Prov`, bukan alokasi Pemprov. Jangan menjumlahkan nasional, `Se-Prov`, provinsi, dan kabupaten/kota pada agregat yang sama karena akan menghitung transfer berulang. Snapshot antarprovinsi saat ini tidak serentak.

## Penanganan status dan edge cases

- `0` berarti sumber secara eksplisit melaporkan realisasi/pagu nol.
- `NOT_AVAILABLE` berarti sumber tidak menyajikan field/observasi.
- `NOT_VERIFIED` berarti ada kandidat data tetapi belum direkonsiliasi.
- `DELAYED` hanya boleh dipakai bila jadwal pembaruan resmi dan tanggal seharusnya tersedia telah diverifikasi. Belum ada dasar untuk rule keterlambatan pada data ini.
- `B = 0`: rasio tidak terdefinisi; tampilkan N/A dan jangan bagi nol.
- `R > B`: jangan batasi rasio ke 100%; tampilkan angka mentah beserta rule review.
- Nilai negatif/koreksi: perlu dukungan field adjustment dan pemeriksaan sumber; jangan diterima otomatis pada input sederhana.
- Jika dua sumber beda angka, simpan keduanya dan catat rekonsiliasi; jangan overwrite tanpa alasan.

## Pesan DSS yang diperbolehkan

Keluaran dukungan keputusan berbentuk langkah pemeriksaan, bukan keputusan kebijakan. Contoh: “Cocokkan nilai pagu/realisasi dengan versi LKPD audited dan snapshot SIKD pada periode yang sama.” Setiap rekomendasi memuat alasan, sumber, dan batas data. Dilarang membuat keputusan penyaluran, menuduh daerah, atau menyimpulkan keterlambatan dari angka agregat tahunan.
