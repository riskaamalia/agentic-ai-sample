"""Dashboard MVP — penjelajah tabel kebutuhan data (D1, D2, ...) dari folder data/.

Jalankan dari root repo:
    .venv/bin/streamlit run app.py      # → http://localhost:8501/data (lihat .streamlit/config.toml)
"""

import pandas as pd
import streamlit as st

from src.show_table import SEMUA_KODE, TABEL

st.set_page_config(page_title="EWS DBH SDA Perikanan", layout="wide")


@st.cache_data(show_spinner="Membaca snapshot data mentah…")
def muat(kode: str) -> tuple[pd.DataFrame, dict]:
    df = TABEL[kode]()
    return df, dict(df.attrs)


st.title("EWS & Simulator DBH SDA Perikanan")
st.caption("Penjelajah data — prototype, bukan sumber angka resmi.")

with st.sidebar:
    kode = st.selectbox(
        "Tabel",
        SEMUA_KODE,
        format_func=lambda k: k if k in TABEL else f"{k} (belum tersedia)",
    )
    if st.button("Muat ulang dari data/"):
        st.cache_data.clear()

if kode not in TABEL:
    st.info(f"{kode} belum tersedia. Sumber datanya belum diverifikasi atau belum diambil.")
    st.stop()

try:
    df, meta = muat(kode)
except FileNotFoundError as e:
    st.error(str(e))
    st.stop()

st.subheader(f"{meta['tabel']} — {meta['judul']}")
st.warning(meta["catatan"])

kiri, tengah, kanan = st.columns(3)
kiri.metric("Jumlah pemda", len(df))
if "Total_Pagu_Rp" in df:
    # Jumlah dari angka yang sudah dibulatkan portal, bukan total resmi.
    miliar = f"{df['Total_Pagu_Rp'].sum() / 1e9:,.2f}".translate(str.maketrans(",.", ".,"))
    tengah.metric("Jumlah pagu (dari angka portal)", f"Rp{miliar} M")
kanan.metric("Pemda tanpa baris akun", meta.get("pemda_tanpa_akun", "-"))

with st.expander("Sumber data"):
    st.write({k: v for k, v in meta.items() if k not in ("tabel", "judul", "catatan")})

cari = st.text_input("Cari nama pemda")
tampil = df[df["Nama_Pemda"].str.contains(cari, case=False, regex=False)] if cari else df

st.dataframe(
    tampil,
    hide_index=True,
    width="stretch",
    column_config={
        kolom: st.column_config.NumberColumn(format="localized")
        for kolom in tampil.columns
        if kolom.endswith("_Rp")
    },
)
st.caption(f"{len(tampil)} dari {len(df)} baris. Sel kosong = data tidak tersedia, bukan nol.")
