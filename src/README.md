# UI Prototype

Vertical slice awal untuk membandingkan baseline dan simulasi DBH SDA Perikanan TA 2024.

## Menjalankan

Dari direktori root repository:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
streamlit run src/app.py
```

## Isi

- `app.py` — UI Streamlit untuk memilih wilayah, melihat data dasar, mengubah input skenario, dan membandingkan rasio/gap.
- `data/observations.json` — fixture kecil dengan URL sumber, snapshot, status ketersediaan, dan presisi.
- `engine/calculations.py` — fungsi hitung Decimal deterministik, tanpa ketergantungan pada UI.

Data contoh SIKD ditampilkan dalam miliar rupiah dan dibulatkan dua desimal. UI menyebut hasil sebagai angka tampilan; jangan menganggapnya nilai rupiah exact. Provinsi Jawa Barat muncul sebagai `not_verified`, bukan nol, dan input skenarionya dinonaktifkan sampai diverifikasi.

Sinyal UI bersifat advisory. Snapshot tahunan tidak cukup untuk menilai keterlambatan penyaluran. Seluruh skenario alternatif diberi label simulasi dan tidak menimpa data sumber.
