Saya sedang membangun proyek **Early Warning System (EWS) DBH SDA Perikanan untuk Kementerian Keuangan Indonesia** sebagai mini SaaS yang berpotensi dikembangkan menjadi produk.

Gunakan dokumen research dan spesifikasi di folder `docs/` sebagai sumber konteks utama.

**Prinsip pengembangan:**
- Gunakan Python untuk backend dan data engineering.
- Mulai dari data publik pemerintah; verifikasi ketersediaan, granularitas, dan frekuensi pembaruan setiap sumber.
- Bangun data pipeline, validasi data, rule engine, dan statistical baseline terlebih dahulu.
- Gunakan FastAPI untuk backend dan Streamlit untuk dashboard MVP.
- Gunakan PostgreSQL untuk penyimpanan awal; pertimbangkan pgvector jika RAG diperlukan.
- Gunakan LangGraph untuk mengorkestrasi AI agent setelah fondasi sistem siap.
- LLM bertugas membantu investigasi, merangkum bukti, dan menjelaskan alert; jangan menjadikannya satu-satunya penentu risiko keuangan.
- Jangan mengarang data, API, regulasi, atau hasil evaluasi.
- Bedakan data yang tidak tersedia, data yang terlambat diperbarui, dan nilai realisasi nol.
- Semua alert AI harus menyertakan bukti dan dapat ditinjau manusia.
- Jangan menulis banyak kode sekaligus. Kerjakan satu tahap, jelaskan alasan desainnya, jalankan pengujian, lalu tunggu persetujuan saya sebelum berpindah ke tahap berikutnya.

**Tugas pertama:** baca semua dokumen proyek yang tersedia, rangkum pemahamanmu, identifikasi informasi yang masih perlu diverifikasi, dan usulkan langkah implementasi pertama. Jangan langsung membangun seluruh aplikasi.