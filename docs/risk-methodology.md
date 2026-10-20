# Metodologi Sinyal dan Perbandingan Skenario

## Tujuan dan batas interpretasi

Engine MVP memberi **sinyal pemantauan** berdasarkan angka pagu/realisasi dan kualitas datanya. Sinyal bukan temuan penyimpangan, prediksi, keputusan penyaluran, atau penilaian kinerja resmi. Istilah “risiko” harus selalu disertai aturan, data, sumber, periode, dan keterbatasan.

DBH SDA Perikanan 2024 adalah data tahunan. Data tersebut tidak menunjukkan tanggal/kurva penyaluran sepanjang tahun, sehingga MVP tidak boleh menyimpulkan terlambat salur.

## Perhitungan deterministik v1

Dengan `B = pagu` dan `R = realisasi`:

1. `rasio_realisasi_pct = R / B × 100`, bila `B > 0` dan kedua nilai tersedia.
2. `sisa_pagu = B - R`, bila kedua nilai tersedia.
3. `selisih_skenario = nilai_skenario - nilai_baseline`.
4. `perubahan_skenario_pct = selisih_skenario / nilai_baseline × 100`, hanya bila baseline tidak nol.

Untuk angka nasional yang ditampilkan SIKD: `B = 951,70` dan `R = 944,29` miliar rupiah. Rasio dari angka tampilan adalah `99,2216…%`, disajikan menjadi **99,22%**. Sisa dari angka tampilan adalah **Rp7,41 miliar**. Angka tersebut direproduksi dari nilai yang telah dibulatkan sumber; jangan menyebutnya nominal exact rupiah.

## Sinyal v1

| Rule ID | Kondisi | Keluaran | Makna |
|---|---|---|---|
| `DQ-001` | Pagu/realisasi hilang atau status belum terverifikasi | `DATA_INCOMPLETE` | Tahan kesimpulan numerik; minta verifikasi sumber. |
| `DQ-002` | Sumber berstatus `ROUNDED_DISPLAY` | `PRECISION_LIMITED` | Boleh hitung demonstrasi pada angka tampilan; hasil bukan nominal presisi penuh. |
| `MON-001` | `R < B` pada snapshot tahunan | `MONITOR_GAP` (advisory) | Ada sisa pagu; bukan bukti keterlambatan/masalah. Tidak ada ambang risiko bisnis pada rule ini. |
| `MON-002` | `R > B` | `REVIEW_OVER_BUDGET` | Minta reviewer memeriksa beda basis, perubahan pagu, koreksi, atau data. Bukan otomatis kesalahan. |
| `MON-003` | Realisasi dibanding tahun sebelumnya berbeda | `YEAR_OVER_YEAR_CHANGE` | Tampilkan besar perubahan dan label “perlu konteks”; jangan menganggap perubahan sebagai anomali tanpa baseline/ambang yang direview. |

Rule adalah aturan demonstrasi yang harus direview ML/BA. MVP tidak menetapkan threshold persentase materialitas karena belum ada ambang resmi yang disetujui.

## Scenario comparison

Skenario baseline menyalin observation dan menyimpan source/version. Skenario alternatif mengubah satu atau lebih input secara eksplisit dan menyimpan catatan asumsi. UI membandingkan pagu, realisasi, rasio, sisa, serta perubahan terhadap baseline. Contoh: baseline nasional `951,70 / 944,29`; alternatif demo mengubah realisasi dengan nilai yang dimasukkan reviewer. Skenario tersebut tidak boleh dilabeli sebagai realisasi resmi atau ramalan.

Perbandingan lintas wilayah harus memberi konteks: nilai nominal, pagu relatif, tahun, sumber, tanggal snapshot, tingkat wilayah, dan presisi. Jangan menambahkan nilai Provinsi Jabar yang belum terverifikasi ke jumlah sampel. Jangan menjumlahkan national, province, dan regency/city pada agregat yang sama karena akan menghitung transfer berulang.

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
