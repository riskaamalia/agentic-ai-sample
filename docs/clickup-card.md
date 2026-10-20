# Pengembangan Engine, UI, dan Scenario Comparison Prototype

## Ringkasan

Bangun vertical slice prototype Early Warning System dan Decision Support System untuk **DBH SDA Perikanan TA 2024**, memakai data publik nasional serta contoh kabupaten/kota di Jawa Barat dan tingkat Provinsi Jawa Barat bila datanya berhasil diverifikasi. Engine bersifat deterministik. UI mendukung input, hasil, dan perbandingan baseline dengan asumsi skenario.

Prototype adalah alat eksplorasi/pemantauan, bukan sistem penetapan alokasi, audit, prediksi, atau keputusan penyaluran resmi.

## Status implementasi

Per 20 Oktober 2026, UI/engine/fixture v0 telah ditulis di `src/`. Pemeriksaan aritmetika dan sintaks dasar dapat dijalankan, tetapi Streamlit belum tersedia di environment saat ini sehingga UI belum dibuka di browser. Review ML/BA dan rekonsiliasi nominal masih pending. Checkbox DoD di bawah tetap belum dicentang sampai bukti runtime dan review tersedia.

## Tujuan

Membuktikan bahwa pengguna dapat memilih/memasukkan data DBH Perikanan, melihat perhitungan yang dapat diulang, membandingkan perubahan asumsi, dan menelusuri sumber serta batasan setiap hasil.

## Ruang lingkup

- Jenis TKD pertama: DBH SDA Perikanan.
- Periode data dasar: TA 2024.
- Cakupan sampel: Nasional, Kota Bandung, Kab. Sumedang, Kab. Bandung Barat, dan Provinsi Jawa Barat ketika observasi tingkat provinsi terverifikasi.
- Metrik v1: pagu, realisasi, persentase realisasi, sisa pagu, perubahan skenario.
- UI MVP: Streamlit; engine Python murni; fixture awal CSV/JSON dengan provenance.
- EWS: sinyal berbasis kualitas data dan rule advisory yang disetujui reviewer.
- DSS: penjelasan bukti dan dampak skenario; manusia tetap mengambil keputusan.

## Definition of Done

- [ ] Prototype dapat dijalankan dari instruksi yang disediakan.
- [ ] Engine deterministik, input UI, output, dan perbandingan skenario tersedia serta dapat diperiksa.
- [ ] Satu jenis TKD dan alur input–hasil–scenario comparison berjalan end-to-end.
- [ ] Minimal satu hasil dihitung ulang terhadap angka acuan; selisih karena pembulatan/basis didokumentasikan.
- [ ] Setiap observasi mempunyai sumber, asumsi, unit, presisi, snapshot, versi, dan batasan yang dapat ditelusuri.
- [ ] Review internal ML/BA dan tindak lanjut tercatat; blocker demo ditutup atau keputusan pengecualian ditulis.

## Acceptance Criteria

### AC-01 — Keluaran

Prototype runnable: engine deterministik, input UI, output dan perbandingan skenario tersedia serta dapat diperiksa.

**Bukti yang direncanakan:** instruksi run; screenshot/rekaman UI; output baseline dan skenario; versi fixture.

### AC-02 — Substansi

Minimal satu jenis TKD (DBH SDA Perikanan), alur input–hasil dan perbandingan skenario berjalan end-to-end.

**Bukti yang direncanakan:** demo memilih observasi 2024, mengubah input simulasi, melihat rasio/gap dan delta.

### AC-03 — Traceability

Minimal satu skenario menghasilkan angka yang sesuai perhitungan acuan atau perbedaan didokumentasikan.

**Acuan awal:** angka nasional SIKD yang tampil: pagu Rp951,70 miliar, realisasi Rp944,29 miliar. Dari angka tampil, rasio = 99,2216…%, dibulatkan menjadi 99,22%, cocok dengan portal. Karena sumber membulatkan angka, validasi nominal exact tetap diperlukan atau pembatasan presisi harus dicantumkan.

### AC-04 — Quality Gate

ML/BA mereview vertical slice dan blocker demo ditindaklanjuti sebelum pengujian final showcase.

**Status saat dokumen dibuat:** belum direview ML/BA. Tidak ada sign-off yang diasumsikan. Lihat `review-log.md` dan `issue-log.md`.

## Acceptance Evidence

Kumpulkan tautan/artefak prototype, sumber data dan fixture versi, output contoh, hasil uji/evaluasi yang benar-benar dijalankan, review internal, decision log, serta issue log. Jangan menulis hasil review atau uji sebelum dilaksanakan.

## Governance

- WP-Reference: `SIKDC-WP07`
- Fast Track: Ya — Showcase W4 November
- Baseline jadwal: 29 Oktober 2026–20 November 2026
- Review internal bukan acceptance kontraktual.

## Keputusan scope dan risiko data

1. Gunakan SIKD sebagai sumber pembanding seragam dan catat snapshot tanggal akses.
2. Sumber SIKD memperlihatkan angka dua desimal dalam miliar; simpan sebagai angka tampilan, jangan mengaku nominal rupiah exact.
3. Observasi Provinsi Jawa Barat belum diisi sampai nilai tingkat provinsi dan definisinya diverifikasi. Nilai tidak tersedia bukan nol.
4. Tidak mengimplementasikan formula Minerba dari diagram untuk DBH Perikanan.
5. Tidak menampilkan alert keterlambatan karena dataset tahunan bukan deret waktu penyaluran.

## Referensi internal

- `research.md` — sumber dan kualitas data.
- `architecture.md` — komponen dan alur.
- `data-model.md` — kontrak observation/scenario/output.
- `risk-methodology.md` — rumus dan aturan sinyal.
- `agent-workflow.md` — alur UI dan review manusia.
- `roadmap.md` — tahap dan gate.
