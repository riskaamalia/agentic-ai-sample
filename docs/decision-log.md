# Decision Log

| ID | Tanggal | Keputusan | Alasan | Konsekuensi/Follow-up | Status |
|---|---|---|---|---|---|
| D-001 | 2026-10-19 | Vertical slice pertama memakai DBH SDA Perikanan TA 2024. | Fokus pada satu jenis TKD dan sesuai card. | Scope lebih luas ditunda. | Disepakati untuk rancangan |
| D-002 | 2026-10-19 | SIKD DJPK menjadi sumber perbandingan awal antarwilayah. | Satu portal menampilkan pagu, realisasi, rasio, dan filter wilayah. | Catat snapshot karena halaman dapat diperbarui. | Disepakati untuk rancangan |
| D-003 | 2026-10-19 | Hasil dari SIKD yang hanya ditampilkan dua desimal miliar diberi status rounded display. | Menghindari klaim rupiah exact yang tak didukung sumber tampilan. | Cari nominal lebih presisi untuk acceptance final. | Disepakati untuk rancangan |
| D-004 | 2026-10-19 | Jangan hitung formula alokasi hukum atau salur ulang dalam MVP. | Sumber yang ditemukan mendukung postur pagu/realisasi, sedangkan formula perikanan belum direkonsiliasi. | Vertical slice berfokus monitoring dan scenario comparison input. | Disepakati untuk rancangan |
| D-005 | 2026-10-19 | Nilai Provinsi Jawa Barat ditandai belum terverifikasi sampai sumber tingkat provinsi ditemukan/cocok. | Menghindari substitusi nilai kosong menjadi nol atau agregat sampel. | Tutup issue `DATA-001` sebelum klaim cakupan provinsi pada demo. | Terbuka |
| D-006 | 2026-10-19 | Belum menambahkan LLM/LangGraph. | Engine hitung harus deterministik dan dapat direview; agent tidak dibutuhkan untuk slice ini. | Pertimbangkan setelah data dan rule stabil. | Disepakati untuk rancangan |

Perubahan keputusan harus menambah baris baru; jangan menghapus riwayat tanpa alasan.
