# Source Code Area

Status: **dashboard Streamlit prototype tersedia**. Dashboard default menampilkan baseline DBH SDA Perikanan TA2026 nasional dan menyediakan observasi TA2025 sebagai historis. Ada sensitivitas skenario sederhana. Data hanya dibaca dari JSON lokal; belum ada API, database, pengambilan otomatis, atau kalkulasi alokasi resmi.

## Struktur saat ini

```text
src/
  app.py                    # dashboard, filter, metrik, grafik, skenario demo
  data/
    observations.json       # fixture kecil dengan sumber dan snapshot
  engine/
    calculations.py         # perhitungan murni yang direncanakan
```

## Menjalankan dashboard

Dari root repository:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run src/app.py --server.baseUrlPath dashboard
```

Buka URL yang ditampilkan Streamlit, biasanya http://localhost:8501/dashboard/.
Jika ingin path tanpa port memakai port 80, perlu reverse proxy atau konfigurasi server lokal.

Fixture TA2026 saat ini baru berisi observasi nasional per 22 Oktober 2026. Fixture TA2025 berisi nasional, Kepri, dan Riau; dua observasi wilayah tersebut merupakan agregat Se-Prov dengan tanggal snapshot berbeda. Jangan mencampur tahun atau menafsirkannya sebagai seluruh 38 provinsi maupun alokasi khusus pemerintah provinsi. Angka tampilan dibulatkan.

Formula alokasi DBH Perikanan belum diimplementasikan. Skenario pada UI hanya sensitivitas asumsi pagu/realisasi untuk demo monitoring, bukan ramalan, hasil alokasi, atau alert resmi.
