# Roadmap Vertical Slice

## Tahap 0 — Scope dan data (selesai sebagai dokumen; implementasi belum dimulai)

- Menetapkan satu jenis TKD: DBH SDA Perikanan TA 2024.
- Menemukan sumber SIKD nasional dan daerah contoh Kota Bandung, Sumedang, Bandung Barat.
- Menandai data tingkat Provinsi Jawa Barat perlu ekstraksi/rekonsiliasi, tidak mengganti dengan nol.
- Menulis prinsip traceability, presisi, dan batas risiko.

## Tahap 1 — Fixture data dan provenance

- Salin fixture kecil dari sumber resmi dengan nominal presisi yang tersedia.
- Simpan angka tampilan, unit, snapshot date, retrieval date, URL dan status.
- Cocokkan satu kasus daerah dengan LKPD audited atau dokumen daerah pada basis sama.
- Putuskan cara menampilkan Provinsi Jawa Barat setelah sumber terverifikasi.

**Gate:** sumber + transkripsi direview sebelum rule/threshold ditambahkan.

## Tahap 2 — Engine deterministik

- Implementasikan validasi dan metrik pagu, realisasi, rasio, gap, delta skenario.
- Implementasikan perlakuan missing/zero/rounded/over-budget dan pembulatan.
- Kunci output fixture nasional pada `99,22%` dari angka tampilan.

**Gate:** acceptance hitung tangan cocok; setiap mismatch dicatat.

## Tahap 3 — UI dan skenario

- Buat Streamlit form untuk memilih observation dan memasukkan asumsi alternatif.
- Tampilkan hasil, bukti, source/version, keterbatasan, dan baseline vs skenario.
- Uji alur end-to-end internal sesuai prosedur proyek.

## Tahap 4 — Quality gate ML/BA

- Reviewer mengisi `review-log.md`.
- Isu demonstrasi dicatat di `issue-log.md`; blocker harus ditutup atau dikecualikan dengan keputusan tertulis.
- Revisi methodology bila reviewer menemukan ambang/interpretasi yang keliru.

## Tahap 5 — Persiapan showcase

- Bekukan versi fixture dan aplikasi.
- Rekam instruksi menjalankan prototype, tangkapan layar/tautan artefak, contoh baseline dan scenario.
- Pastikan bukti AC-01 sampai AC-04 siap dan keterbatasan dijelaskan.

## Jadwal dari card

Baseline card adalah 29 Oktober–20 November 2026, showcase W4 November. Jadwal internal detail belum disepakati. Urutkan pekerjaan berdasarkan dependency dan sisakan waktu untuk review; jangan menandai milestone tercapai hanya karena dokumen desain selesai.
