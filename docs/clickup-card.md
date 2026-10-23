# Pengembangan Engine, UI, dan Scenario Comparison Prototype

## Ringkasan

Bangun vertical slice prototype **pemantauan dan scenario comparison DBH SDA Perikanan TA 2026** sebagai use case EWS/DSS SIKD Cerdas. Baseline awal memakai data nasional berjalan; perluasan ke seluruh provinsi mengikuti verifikasi data wilayah. Ikuti alur input dan parameter → validasi → keluaran keputusan yang dapat dibandingkan dan ditelusuri. SIKD `Se-Prov` berarti agregat se-provinsi, bukan otomatis alokasi kepada pemerintah provinsi.

Prototype adalah alat analisis untuk mendukung keputusan; hasilnya bukan penetapan alokasi final, audit, prediksi, atau keputusan penyaluran resmi. UI input awal kini tersedia di `src/app.py`, tetapi engine, hasil alokasi, dan perbandingan keluaran belum tersedia; card belum runnable end-to-end.

## Tujuan

Membuktikan satu alur end-to-end yang bisa diperiksa: pengguna memilih atau memasukkan data dan parameter DBH Perikanan, sistem memvalidasi kelengkapan dan provenance, mesin deterministik menjalankan formula yang telah diverifikasi untuk versi/periode terkait, lalu UI menyajikan estimasi per daerah, perbandingan skenario, selisih terhadap pagu/periode acuan, dan jejak perhitungan. Setiap hasil menyertakan sumber, asumsi, versi formula, serta batas interpretasi.

## Ruang lingkup

- Jenis TKD pertama: DBH SDA Perikanan.
- Periode data dasar: TA2026; TA2025 menjadi data historis bila definisi dan basisnya sebanding.
- Cakupan observasi awal: nasional TA2026. Cakupan target: agregat `Se-Prov` seluruh provinsi setelah snapshot TA2026 tiap wilayah tersedia dan diverifikasi.
- Cakupan mesin alokasi: tetap memerlukan data penerima pada tingkat kabupaten/kota secara nasional dan aturan lengkap; agregat provinsi saja tidak cukup untuk mereproduksi formula alokasi.
- Input: penerimaan DBH Perikanan, wilayah penerima/hirarki wilayah, variabel dan bobot yang bersumber dari regulasi, data historis, serta pagu indikatif. Status ketersediaan, satuan, snapshot, dan versi sumber wajib eksplisit.
- Mesin simulasi: validasi kelengkapan; formula alokasi yang diverifikasi untuk DBH Perikanan; perubahan parameter antar-skenario; rekonsiliasi total hasil terhadap pagu acuan.
- Output: estimasi per daerah, perbandingan skenario, selisih antarperiode dan terhadap pagu, serta jejak input–formula–hasil untuk review.
- UI MVP: Streamlit; engine Python deterministik; fixture CSV/JSON berversi dengan provenance.
- EWS: sinyal awal berfokus pada kualitas/kelengkapan data dan aturan advisory yang direview; jangan menyimpulkan keterlambatan dari data agregat tahunan.
- DSS: memperlihatkan konsekuensi perubahan asumsi dan bukti pendukung; keputusan tetap pada manusia.
- Model target dibatasi pada satu jenis TKD agar arsitektur dapat dikembangkan ke jenis TKD lain tanpa mengklaim formula lintas jenis sudah tersedia.

**Batas penting:** formula/bobot DBH Perikanan tidak boleh ditebak atau diambil dari diagram DBH Minerba. Sampai sumber hukum, variabel, bobot, dan basis datanya dikonfirmasi, alokasi per daerah serta rekonsiliasi pagu adalah kebutuhan target yang berstatus blocked; angka pagu/realisasi yang telah tersedia hanya mendukung demonstrasi monitoring/perbandingan, bukan simulasi alokasi.

## Definition of Done

- [ ] Prototype dapat dijalankan dari instruksi yang disediakan.
- [ ] Input, validasi, engine deterministik, output alokasi, dan perbandingan skenario tersedia serta dapat diperiksa.
- [ ] DBH SDA Perikanan dan alur data–formula–hasil–scenario comparison berjalan end-to-end.
- [ ] Total alokasi skenario direkonsiliasi terhadap pagu acuan; selisih atau pembatasan basis didokumentasikan.
- [ ] Minimal satu skenario dihitung ulang terhadap angka acuan independen; perbedaan dijelaskan.
- [ ] Setiap data/parameter menyimpan sumber, asumsi, unit, presisi, snapshot, versi regulasi/formula, dan batasan.
- [ ] Hasil menampilkan estimasi per daerah, perubahan terhadap baseline/pagu, dan jejak hitung.
- [ ] Review internal ML/BA dan tindak lanjut tercatat; blocker demo ditutup atau pengecualian diputuskan tertulis.

## Acceptance Criteria

### AC-01 — Keluaran

Prototype runnable: engine deterministik, input UI, output dan perbandingan skenario tersedia serta dapat diperiksa.

**Bukti yang direncanakan:** instruksi run; screenshot/rekaman UI; input tervalidasi; output baseline dan skenario; rekonsiliasi; versi fixture/formula; jejak hitung.

### AC-02 — Substansi

Minimal satu jenis TKD (DBH SDA Perikanan), alur input–hasil dan perbandingan skenario berjalan end-to-end.

**Bukti yang direncanakan:** demo memilih data/parameter DBH Perikanan TA2026, menjalankan estimasi alokasi per daerah, mengubah asumsi skenario, lalu melihat delta dan rekonsiliasi pagu. Saat ini baru monitoring nasional TA2026 yang tersedia di fixture. Sebelum formula dan dataset penerima terverifikasi, demonstrasi monitoring belum memenuhi substansi simulasi alokasi.

### AC-03 — Traceability

Minimal satu skenario menghasilkan angka yang sesuai perhitungan acuan atau perbedaan didokumentasikan.

**Acuan awal yang tersedia:** snapshot SIKD nasional TA2026 per 22 Oktober 2026 menampilkan pagu 225,90 M dan realisasi 183,47 M (81,22%). Hitungan dari angka tampilan menghasilkan gap 42,43 M; ini hanya pemeriksaan monitoring, bukan validasi formula alokasi atau angka final tahunan. AC-03 tetap memerlukan satu skenario yang dicocokkan dengan acuan resmi independen.

### AC-04 — Quality Gate

ML/BA mereview vertical slice dan blocker demo ditindaklanjuti sebelum pengujian final showcase.

**Status saat dokumen diperbarui:** belum direview ML/BA. Tidak ada sign-off yang diasumsikan. Reviewer juga perlu menyetujui interpretasi formula, rekonsiliasi pagu, dan wording EWS/DSS. Lihat `review-log.md` dan `issue-log.md`.

## Acceptance Evidence

Kumpulkan tautan/artefak prototype, sumber data dan fixture versi, output contoh, hasil uji/evaluasi yang benar-benar dijalankan, review internal, decision log, serta issue log. Jangan menulis hasil review atau uji sebelum dilaksanakan.

## Governance

- WP-Reference: `SIKDC-WP07`
- Fast Track: Ya — Showcase W4 November
- Baseline jadwal: 29 Oktober 2026–20 November 2026
- Review internal bukan acceptance kontraktual.

## Keputusan scope dan risiko data

1. Gunakan SIKD sebagai sumber observasi/pembanding seluruh provinsi dan catat tanggal snapshot per halaman; jangan menganggap pagu/realisasi `Se-Prov` sebagai data dasar formula alokasi atau pagu khusus Pemprov.
2. Sumber SIKD memperlihatkan angka dua desimal dalam miliar; simpan sebagai angka tampilan, jangan mengaku nominal rupiah exact.
3. Jangan menyamakan agregat `Se-Prov` dengan entitlement pemerintah provinsi. Jika observasi wilayah tidak tersedia, bedakan `NOT_AVAILABLE`, `NOT_VERIFIED`, dan nol yang dilaporkan sumber.
4. Tidak mengimplementasikan formula Minerba dari diagram untuk DBH Perikanan. Variabel dan bobot harus diverifikasi dari dasar hukum DBH Perikanan yang relevan.
5. Tidak menampilkan alert keterlambatan karena dataset tahunan bukan deret waktu penyaluran.
6. Diagram menyebut Cetak Biru SIKD 2025–2029/KEP-65/PK/2025; identitas dan dokumen resminya belum berhasil diverifikasi dari pencarian yang dilakukan. Perlakukan sebagai rujukan dari materi yang diberikan, bukan fakta hukum terkonfirmasi, sampai tautan/dokumen primer diperoleh.

## Referensi internal

- `research.md` — sumber dan kualitas data.
- `architecture.md` — komponen dan alur.
- `data-model.md` — kontrak observation/scenario/output.
- `risk-methodology.md` — rumus dan aturan sinyal.
- `agent-workflow.md` — alur UI dan review manusia.
- `roadmap.md` — tahap dan gate.
