# src/

Kode Python proyek. Jalankan semua perintah dari root repo; entry point dashboard ada di `../app.py`.

```text
src/
  ingest/
    fetch_raw.py      # unduh data mentah ke data/raw/ + source.json (CLI)
  tables/
    portal_tkdd.py    # baca snapshot Portal TKDD: pilih snapshot, parse ekspor, konversi nilai
    d01.py            # load_d01(): D1 Pagu DBH SDA Perikanan per pemda → DataFrame
  show_table.py       # registri tabel D1–D12 yang dipakai dashboard
```

Alur data: `ingest` mengambil file mentah apa adanya → `tables` membaca file mentah menjadi DataFrame per
kelompok data (D1, D2, …) → `app.py` menampilkannya.

Menambah tabel baru: buat `tables/dNN.py` dengan fungsi `load_dNN()` yang mengembalikan DataFrame (dengan
`df.attrs` berisi `tabel`, `judul`, `catatan`, dan info sumber), lalu daftarkan di `TABEL` pada
`show_table.py`.
