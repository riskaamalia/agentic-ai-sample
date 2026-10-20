# Source Code Area

Status: **belum ada kode aplikasi**. Folder ini saat ini hanya menyimpan dokumen kontrak awal agar implementasi tetap bertahap dan mudah direview.

## Rencana modul pertama

```text
src/
  app.py                    # entry point Streamlit
  engine/
    calculations.py         # rasio, gap, delta scenario; pure functions
    validation.py           # validasi nilai/status/provenance
  data/
    observations.csv        # fixture DBH Perikanan berversi
    loader.py               # parsing tanpa kehilangan metadata
  ui/
    components.py           # tampilan hasil/source/scenario bila dibutuhkan
```

Mulai dengan fixture dan engine saja. Tambahkan satu tahap pada satu waktu. Jangan buat folder/file Python di sini sebelum definisi dan ruang lingkup tahap implementasinya siap direview.

Kontrak desain ada di `../docs/architecture.md`, `../docs/data-model.md`, dan `../docs/risk-methodology.md`.
