# Model Data Prototype

## Prinsip

Model memisahkan **nilai sumber**, **perhitungan aplikasi**, dan **hasil skenario**. Nilai dari portal dengan pembulatan tidak boleh disimpan seolah nominalnya exact. Missing, nol, dan belum diverifikasi adalah status berbeda.

## Entitas `Observation`

| Field | Tipe konseptual | Contoh | Keterangan |
|---|---|---|---|
| `observation_id` | string | `sikd-2026-national-perikanan` | ID stabil untuk fixture. |
| `fiscal_year` | integer | `2026` | Tahun anggaran. |
| `fund_type` | enum | `DBH_SDA_PERIKANAN` | MVP hanya mendukung satu jenis TKD. |
| `region_code` | string/null | `3273` atau null | Kode wilayah perlu disepakati dari sumber baku; jangan menebak. |
| `region_name` | string | `Kota Bandung` | Simpan nama yang ditampilkan sumber. |
| `region_level` | enum | `NATIONAL`, `SE_PROVINCE`, `PROVINCE`, `REGENCY`, `CITY` | `SE_PROVINCE` adalah agregat seluruh wilayah dalam provinsi; bukan entitas Pemprov. Jangan menjumlahkan tingkat yang tumpang tindih. |
| `budget_rupiah` | integer/null | `1070000000` (perkiraan dari tampilan 1,07 miliar) | Jika nominal exact tidak tersedia, jangan mengisi field ini dengan perkiraan; gunakan `display_value` di bawah. |
| `realization_rupiah` | integer/null | null | Rupiah exact bila sumber menyediakan. |
| `display_budget` | Decimal/string/null | `1.07` | Nilai seperti tampil di sumber. |
| `display_realization` | Decimal/string/null | `1.07` | Nilai seperti tampil di sumber. |
| `display_unit` | enum | `IDR_BILLION` | Satuan yang ditampilkan; contoh di SIKD menggunakan miliar rupiah. |
| `precision_status` | enum | `ROUNDED_DISPLAY` | `EXACT_SOURCE`, `ROUNDED_DISPLAY`, `UNKNOWN`. |
| `value_status` | enum | `AVAILABLE` | `AVAILABLE`, `ZERO`, `NOT_AVAILABLE`, `NOT_VERIFIED`. Status nol hanya untuk nol yang dinyatakan sumber. |
| `source_id` | string | `SOURCES-SIKD-2026-NATIONAL` | Relasi ke sumber dan snapshot. |
| `source_as_of` | date/null | `2026-10-18` | Tanggal snapshot menurut halaman. |
| `retrieved_at` | datetime | timestamp proses ekstraksi | Tanggal saat fixture ditranskripsi. |
| `notes` | string | `Miliar, dibulatkan 2 desimal` | Catatan basis, mismatch, atau reviewer. |

Catatan: angka nasional TA2026 yang tampil (pagu 225,90 M, realisasi 183,47 M) dapat disimpan pada `display_*` dengan status `ROUNDED_DISPLAY`; jangan konversi angka tampilan menjadi nominal exact rupiah. Snapshot 2026 adalah data berjalan. Untuk agregat filter provinsi gunakan tingkat `SE_PROVINCE`, bukan `PROVINCE`.

## Entitas `Scenario`

| Field | Makna |
|---|---|
| `scenario_id` | ID scenario unik. |
| `label` | `Baseline`, `Input pengguna`, atau label lain. |
| `observation_id` | Data dasar yang diubah. |
| `budget_override` / `realization_override` | Nilai alternatif, dengan satuan dan presisi eksplisit. |
| `assumption_note` | Alasan/asal input alternatif. Wajib untuk skenario buatan pengguna. |
| `created_by` | Pengguna atau `demo_fixture`. |
| `created_at` | Waktu pembuatan. |

Skenario alternatif tidak menimpa Observation dan tidak disebut nilai aktual. UI harus memberi label “simulasi/asumsi”.

## Entitas target simulator alokasi

Entitas berikut diperlukan sebelum klaim “simulasi alokasi” dapat diterima. Nilainya tidak boleh diisi dari tebakan atau disimpulkan hanya dari pagu/realisasi SIKD.

| Entitas | Field minimum | Alasan |
|---|---|---|
| `AllocationInput` | `fiscal_year`, `fund_type`, total penerimaan/basis alokasi, `region_code`, `region_level`, variabel formula, nilai, unit, status, `source_id` | Menyimpan nilai masukan formula beserta wilayah dan asalnya. |
| `FormulaVersion` | `formula_id`, `version`, `legal_reference`, tanggal berlaku, variabel, bobot/koefisien, aturan pembulatan, catatan interpretasi, status review | Menjaga formula tetap berversi dan dapat ditelusuri ke aturan. |
| `ScenarioParameter` | `scenario_id`, parameter, nilai baseline, nilai override, unit, alasan, pencipta | Membuat perubahan asumsi tampak jelas dan tidak mengubah data sumber. |
| `AllocationResult` | wilayah, nilai hasil, komponen hitung, `formula_version`, `scenario_id`, total pagu acuan, total hasil, residual rekonsiliasi | Memungkinkan hasil per daerah serta pemeriksaan bahwa totalnya konsisten dengan basis. |

Apabila bobot atau aturan lintas wilayah belum dapat dipetakan secara sah, sistem harus berhenti dengan status `FORMULA_UNVERIFIED`; jangan mengeluarkan angka alokasi yang tampak resmi.

## Entitas `CalculationResult`

Simpan metrik, input yang dipakai, formula/version, waktu hitung, dan status. Metrik minimum:

- `realization_ratio = realization / budget × 100`, bila keduanya tersedia dan `budget > 0`;
- `budget_gap = budget - realization`, bila keduanya tersedia;
- `scenario_delta = scenario_metric - baseline_metric`;
- `scenario_delta_pct`, hanya jika baseline bukan nol.

Engine menggunakan Decimal atau integer rupiah. Pembulatan untuk UI dilakukan hanya pada lapisan presentasi dan aturan pembulatan diberi versi.

## Entitas `Alert` dan `Review`

Alert menyimpan `rule_id`, severity, deskripsi, evidence/input IDs, rule version, status kualitas data, dan `human_review_required=true`. Review menyimpan reviewer, peran, tanggal, status, keputusan, komentar, dan issue tindak lanjut. Tidak ada alert otomatis pada wilayah yang status datanya `NOT_AVAILABLE` atau `NOT_VERIFIED`.

## Kontrak serialisasi fixture

Fixture CSV/JSON mencakup semua field provenance di atas. Untuk versi pertama gunakan nilai `display_*` persis sesuai teks sumber dan kosongkan nominal rupiah exact bila tidak tersedia. Mapping nama akun ke `DBH_SDA_PERIKANAN` dicatat di mapping berversi, termasuk kode rekening jika sumber daerah memakai kode berbeda.
