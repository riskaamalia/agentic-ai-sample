# Roadmap Vertical Slice

## Tahap 0 — Scope dan data (dokumen awal tersedia; scope target diperjelas)

- Menetapkan satu jenis TKD: DBH SDA Perikanan TA2026.
- Menetapkan baseline monitoring nasional TA2026 yang berjalan; perluasan ke agregat `Se-Prov` dilakukan setelah observasi tiap wilayah tersedia dan diverifikasi.
- Memisahkan kebutuhan dashboard agregat dari kebutuhan formula alokasi yang memerlukan seluruh kabupaten/kota nasional.
- Menulis prinsip traceability, presisi, dan batas risiko.
- Menyelaraskan target card dengan diagram: input/parameter → validasi/formula → estimasi per daerah, perbandingan skenario, rekonsiliasi, dan audit trail.
- Membatasi hasil saat ini: monitoring pagu/realisasi bukan simulasi formula alokasi.
- UI awal untuk input data/provenance/variabel/asumsi skenario tersedia di `src/app.py`; belum menjadi vertical slice runnable atau dihitung end-to-end.

## Tahap 1 — Verifikasi substansi alokasi dan fixture data

- Temukan dasar hukum DBH Perikanan untuk tahun/jenis proses yang disimulasikan, formula, variabel, bobot, penerima, dan aturan pembulatan.
- Ekstrak snapshot SIKD TA2026 untuk nasional dan target 38 agregat provinsi; catat snapshot per wilayah dan jangan membandingkan tanggal yang tidak serentak.
- Verifikasi pagu APBN dan penyesuaian alokasi TA2026 pada sumber resmi; catat versi baseline dan tanggal berlaku.
- Temukan basis PNBP, luas laut, IKLH/kriteria kinerja, serta contoh alokasi resmi tingkat penerima yang cukup untuk menghitung ulang satu kasus.
- Salin fixture resmi beserta unit, snapshot date, retrieval date, URL, presisi, provenance, dan status verifikasi.
- Rekonsiliasi setidaknya satu daerah dan total nasional/pagu. Putuskan tampilan Provinsi Jabar setelah sumber terverifikasi.

**Gate blocker:** formula, aturan TA2026, dan angka acuan resmi disetujui reviewer domain. Jika belum tersedia, jangan implementasikan output alokasi; tandai demonstrasi nasional sebagai monitoring sementara dan minta keputusan stakeholder.

## Tahap 2 — Kontrak data dan engine deterministik

- Implementasikan skema input, provenance, hierarki wilayah, formula version, dan status data.
- Implementasikan formula alokasi hanya dari aturan terverifikasi; hitung estimasi per daerah, residual rekonsiliasi, dan delta antar-skenario.
- Implementasikan perlakuan missing/zero/rounded/over-budget dan aturan pembulatan yang bersumber.
- Pertahankan hitung 99,22% SIKD hanya sebagai pemeriksaan monitoring terpisah, bukan bukti formula alokasi.

**Gate:** hitung tangan/acuan resmi cocok; mismatch, basis dan residual dicatat.

## Tahap 3 — UI dan skenario

- Buat Streamlit form untuk memilih data/parameter dan membuat asumsi skenario.
- Tampilkan estimasi alokasi per daerah, rekonsiliasi, bukti, source/formula version, keterbatasan, dan baseline vs skenario.
- Uji alur end-to-end internal sesuai prosedur proyek.

## Tahap 4 — Quality gate ML/BA

- Reviewer mengisi `review-log.md`.
- Isu demonstrasi dicatat di `issue-log.md`; blocker harus ditutup atau dikecualikan dengan keputusan tertulis.
- Revisi methodology bila reviewer menemukan ambang/interpretasi yang keliru.
- Review kecocokan formula, variabel/bobot DBH Perikanan, total alokasi terhadap pagu, dan apakah wording cukup jelas bahwa hasil bukan alokasi final.

## Tahap 5 — Persiapan showcase

- Bekukan versi fixture dan aplikasi.
- Rekam instruksi menjalankan prototype, tangkapan layar/tautan artefak, contoh baseline dan scenario.
- Pastikan bukti AC-01 sampai AC-04 siap dan keterbatasan dijelaskan.

## Ketergantungan kritis

Snapshot nasional TA2026 memungkinkan dashboard pemantauan berjalan, tetapi belum menyediakan perbandingan antarwilayah dan belum memenuhi AC-02/AC-03 sebagai simulator alokasi per penerima. Dibutuhkan data TA2026 per wilayah, input seluruh penerima, rincian formula yang berlaku, dan contoh angka acuan. Data TA2025 hanya dipakai sebagai historis setelah basisnya disetarakan.

## Jadwal dari card

Baseline card adalah 29 Oktober–20 November 2026, showcase W4 November. Jadwal internal detail belum disepakati. Urutkan pekerjaan berdasarkan dependency dan sisakan waktu untuk review; jangan menandai milestone tercapai hanya karena dokumen desain selesai.
