# Issue dan Blocker Log

| ID | Severity | Isu | Dampak | Tindak lanjut | Owner | Status |
|---|---|---|---|---|---|---|
| DATA-001 | Blocker untuk klaim cakupan Provinsi Jabar | Nominal DBH SDA Perikanan TA 2024 untuk entitas Provinsi Jawa Barat belum diekstrak dan direkonsiliasi. | Tidak boleh menampilkan nol atau menyatakan total provinsi tersedia. | Ambil tabel rinci LRA/CaLK Pemprov Jabar audited dan filter wilayah SIKD; dokumentasikan basis serta perbedaan. | Belum ditetapkan | Open |
| DATA-002 | High | SIKD menampilkan nominal daerah dalam satuan miliar dengan dua desimal. | Tidak cukup untuk acceptance nominal exact rupiah. | Minta/temukan ekspor atau cocokkan nominal penuh pada LKPD daerah. | Belum ditetapkan | Open |
| DATA-003 | Medium | Ketersediaan API/ekspor SIKD dan frekuensi pembaruan belum diverifikasi. | Otomasi pipeline belum direncanakan. | Verifikasi manual/ketentuan penggunaan; prototype pakai fixture berversi. | Belum ditetapkan | Open |
| RULE-001 | High | Belum ada ambang materialitas/risiko yang disetujui ML/BA. | Sinyal hanya advisory; tidak boleh menyebut risiko resmi. | Minta reviewer menyetujui rule atau biarkan hanya status monitoring/data quality. | Reviewer ML/BA | Open |
| GOV-001 | Blocker sebelum final showcase | Review internal belum dilakukan dan belum ada bukti runtime prototype. | AC-01 dan AC-04 belum terpenuhi. | Implementasi slice, jalankan sesuai rencana verifikasi, minta review, tutup blocker demo. | Belum ditetapkan | Open |

Blocker dianggap tertutup hanya setelah ada bukti atau keputusan tertulis beserta penanggung jawab.
