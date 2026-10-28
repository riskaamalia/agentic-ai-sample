# data/

Penyimpanan data tahap awal (belum memakai database).

## raw/

File asli dari sumber (unduhan portal, lampiran peraturan, hasil scraping), disimpan **apa adanya** — jangan
diedit. Satu folder per sumber dan waktu akses (memuat jam, karena portal bisa berubah dalam hari yang sama):

```
raw/<sumber>/<YYYY-MM-DDTHHMMSS>/
  <file asli>      mis. lampiran PDF, ekspor XLSX/CSV, HTML
  source.json      metadata sumber
```

Isi folder ini dibuat oleh script, bukan diunduh manual. Untuk mengambil snapshot baru (dari root repo):

```
.venv/bin/python -m src.ingest.fetch_raw portal-tkdd --tahun 2026   # ±10 menit, ±620 permintaan
.venv/bin/python -m src.ingest.fetch_raw perpres-118-2025           # PDF ±21 MB
```

Snapshot lama tidak ditimpa; setiap pengambilan membuat folder baru.

Isi `data/` (kecuali README ini dan `raw/.gitkeep`) **tidak masuk git** — lihat `.gitignore`. Setiap anggota tim
mengambil snapshot sendiri dengan script di atas; `sha256` di `source.json` dipakai untuk memastikan file
yang sama.

Isi minimum `source.json`:

```json
{
  "sumber": "Nama portal / dokumen",
  "url": "https://...",
  "tanggal_akses": "YYYY-MM-DDTHH:MM:SS+07:00",
  "tanggal_snapshot": "YYYY-MM-DD atau null bila tidak diketahui",
  "kelompok_data": "D1",
  "catatan": "cakupan, keterbatasan, status verifikasi"
}
```

## Konvensi data olahan

- Data tabular (D1–D12) → CSV; parameter, ambang R1–R7, dan metadata → JSON.
- Nominal Rupiah sebagai bilangan bulat rupiah.
- Sel kosong = **tidak tersedia**; `0` = **nilai nol**. Jangan mengisi kosong dengan 0.
- Data terlambat diperbarui ditandai lewat `tanggal_snapshot` di metadata, bukan di sel data.
- Data sintetis untuk pengujian tidak disimpan di sini, melainkan di fixture `tests/`.
