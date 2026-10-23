"""Streamlit dashboard for DBH SDA Perikanan public observations."""

from __future__ import annotations

import json
from decimal import Decimal
from pathlib import Path

import pandas as pd
import streamlit as st

from engine.monitoring import Observation, ScenarioOverride, build_evidence_packet, run_scenario


DATA_PATH = Path(__file__).parent / "data" / "observations.json"

st.set_page_config(
    page_title="Dashboard DBH Perikanan",
    page_icon="🐟",
    layout="wide",
    initial_sidebar_state="expanded",
)


@st.cache_data
def load_observations() -> pd.DataFrame:
    """Load the small, source-linked public demo fixture."""
    with DATA_PATH.open(encoding="utf-8") as file:
        records = json.load(file)
    return pd.DataFrame(records)


def money(value: float | Decimal) -> str:
    billions = float(value) / 1_000
    return f"Rp{billions:,.2f} miliar".replace(",", "_").replace(".", ",").replace("_", ".")


observations = load_observations()

with st.sidebar:
    st.markdown("## 🐟 SIKD Cerdas")
    st.caption("Dashboard pemantauan · Prototype")
    st.divider()
    available_years = sorted(observations.fiscal_year.unique().tolist(), reverse=True)
    fiscal_year = st.selectbox("Tahun anggaran", available_years, index=0)
    year_observations = observations.loc[observations.fiscal_year == fiscal_year]
    province_names = year_observations.loc[
        year_observations.region_level == "SE_PROVINCE", "region_name"
    ].tolist()
    region_options = ["Nasional", *province_names]
    if province_names:
        region_options.insert(1, "Semua agregat Se-Prov")
    selected_region = st.selectbox(
        "Wilayah", region_options
    )
    st.divider()
    st.markdown("**Status substansi**")
    st.warning("Monitoring pagu/realisasi. Belum menghitung ulang formula alokasi.")
    st.caption("Angka berasal dari tampilan publik SIKD, dalam juta rupiah.")

st.markdown(
    """
    <style>
    .block-container {padding-top:1.7rem; padding-bottom:2.5rem; max-width:1440px;}
    div[data-testid="stMetric"] {background:#f4f8fb; border:1px solid #e2ebf1; padding:16px 18px; border-radius:12px;}
    div[data-testid="stMetricLabel"] p {color:#536777;}
    a {text-decoration:none;}
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("Dashboard DBH SDA Perikanan")
st.caption(f"Tahun Anggaran {fiscal_year} · Early Warning System & Decision Support System")

year_observations = observations.loc[observations.fiscal_year == fiscal_year]
province_rows = year_observations.loc[year_observations.region_level == "SE_PROVINCE"].copy()

if selected_region == "Nasional":
    current = year_observations.loc[year_observations.region_level == "NATIONAL"]
elif selected_region == "Semua agregat Se-Prov":
    current = province_rows
else:
    current = province_rows.loc[province_rows.region_name == selected_region]

if current.empty:
    st.error("Belum ada observasi untuk filter ini.")
    st.stop()

budget_total = float(current.budget_million_idr.sum())
realized_total = float(current.realization_million_idr.sum())
ratio = realized_total / budget_total * 100 if budget_total else 0.0
gap = budget_total - realized_total

st.markdown("### Ringkasan pemantauan")
metric_cols = st.columns(4)
metric_cols[0].metric("Pagu terpilih", money(budget_total))
metric_cols[1].metric("Realisasi terpilih", money(realized_total))
metric_cols[2].metric("Rasio realisasi", f"{ratio:.2f}%")
metric_cols[3].metric("Selisih pagu–realisasi", money(gap))

if selected_region == "Semua agregat Se-Prov":
    st.info(
        "Jumlah pada tampilan ini hanya menjumlahkan dua contoh agregat yang tersedia "
        "(Kepri dan Riau), bukan total Indonesia. Snapshot keduanya berbeda tanggal; "
        "jangan gunakan angka ini sebagai total se-Indonesia atau perbandingan serentak."
    )
elif selected_region == "Nasional":
    st.info(
        "Nilai nasional mengikuti tampilan SIKD dan dibulatkan dua desimal; "
        "hasil rasio hanya cocok untuk pemeriksaan angka tampilan."
    )
else:
    row = current.iloc[0]
    if row.region_level == "NATIONAL":
        st.info(f"Snapshot nasional SIKD: {row.snapshot_date}. Nilai tampilan dibulatkan.")
    else:
        st.info(
            f"{row.region_name} adalah agregat Se-Prov, bukan alokasi khusus pemerintah "
            f"provinsi. Snapshot: {row.snapshot_date}."
        )

left, right = st.columns([1.45, 1])
with left:
    st.markdown("### Perbandingan wilayah tersedia")
    if province_rows.empty:
        st.info(f"Observasi SIKD tingkat Se-Prov TA {fiscal_year} belum tersedia dalam fixture.")
    else:
        display = province_rows[
            ["region_name", "budget_million_idr", "realization_million_idr", "snapshot_date"]
        ].copy()
        display["Rasio"] = (
            display.realization_million_idr / display.budget_million_idr * 100
        ).map(lambda value: f"{value:.2f}%")
        display = display.rename(
            columns={
                "region_name": "Agregat Se-Prov",
                "budget_million_idr": "Pagu (Rp juta)",
                "realization_million_idr": "Realisasi (Rp juta)",
                "snapshot_date": "Snapshot",
            }
        )
        st.dataframe(
            display,
            hide_index=True,
            use_container_width=True,
            column_config={
                "Pagu (Rp juta)": st.column_config.NumberColumn(format="%,.2f"),
                "Realisasi (Rp juta)": st.column_config.NumberColumn(format="%,.2f"),
            },
        )
        st.caption("Observasi yang tersimpan belum mewakili seluruh 38 provinsi.")

with right:
    st.markdown("### Pagu dan realisasi")
    if province_rows.empty:
        st.caption("Grafik perbandingan provinsi akan muncul setelah observasi Se-Prov tahun ini diverifikasi.")
    else:
        chart_data = province_rows.set_index("region_name")[
            ["budget_million_idr", "realization_million_idr"]
        ]
        chart_data.columns = ["Pagu", "Realisasi"]
        st.bar_chart(chart_data, color=["#1b4965", "#159a91"], height=250)
        st.caption("Satuan grafik: Rp juta. Nilai sumber yang ditampilkan SIKD dapat dibulatkan.")

st.divider()
st.markdown("### Perbandingan skenario (asumsi pengguna)")
st.caption(
    "Ubah asumsi pagu dan/atau realisasi; engine menghitung ulang dan menyusun paket bukti. "
    "Ini bukan ramalan dan bukan formula alokasi DBH."
)
scenario_left, scenario_right = st.columns([1, 2])
with scenario_left:
    scenario_region = st.selectbox(
        "Basis skenario", year_observations.region_name.tolist(), key="scenario_region"
    )
    budget_change_pct = st.slider("Perubahan pagu asumsi (%)", -50, 50, 0, 1)
    realization_change_pct = st.slider("Perubahan realisasi asumsi (%)", -50, 50, 5, 1)
    assumption_note = st.text_area(
        "Catatan asumsi (wajib)",
        value="Contoh demo: penyesuaian asumsi untuk melihat dampak terhadap rasio dan sisa pagu.",
    )
base_row = year_observations.loc[year_observations.region_name == scenario_region].iloc[0]
base_observation = Observation.from_record(base_row.to_dict())
comparison = None
scenario_error = None
if base_observation.budget is None or base_observation.realization is None:
    scenario_error = "Observasi basis tidak memiliki pagu/realisasi; skenario tidak dihitung."
else:
    try:
        override = ScenarioOverride(
            scenario_id=f"demo-{base_observation.observation_id}",
            label="Asumsi pengguna",
            assumption_note=assumption_note,
            budget=base_observation.budget * (1 + Decimal(budget_change_pct) / 100),
            realization=base_observation.realization * (1 + Decimal(realization_change_pct) / 100),
        )
        comparison = run_scenario(base_observation, override)
    except ValueError as error:
        scenario_error = str(error)

with scenario_right:
    if comparison is None:
        st.error(scenario_error)
    else:
        base, alt = comparison.baseline, comparison.scenario
        ratio_text = lambda value: "N/A" if value is None else f"{value:.2f}%"
        table = pd.DataFrame(
            {
                "Metrik": ["Pagu", "Realisasi", "Rasio realisasi", "Sisa pagu"],
                "Baseline (SIKD)": [money(base.budget), money(base.realization),
                                    ratio_text(base.ratio_pct), money(base.gap)],
                "Skenario (asumsi)": [money(alt.budget), money(alt.realization),
                                      ratio_text(alt.ratio_pct), money(alt.gap)],
            }
        )
        st.dataframe(table, hide_index=True, use_container_width=True)
        st.markdown("**Sinyal pada skenario** (advisory, perlu review manusia)")
        for signal in alt.signals:
            st.markdown(f"- `{signal['rule_id']}` {signal['output']} — {signal['message']}")
        with st.expander("Paket bukti (evidence packet) untuk review / penjelasan LLM"):
            st.json(build_evidence_packet(comparison))

with st.expander("Sumber, definisi, dan batas interpretasi", expanded=False):
    st.markdown("**Sumber observasi**")
    for _, item in year_observations.iterrows():
        st.markdown(
            f"- **{item.region_name}** — snapshot {item.snapshot_date}; "
            f"[buka sumber SIKD]({item.source_url})"
        )
    st.markdown(
        """
        **Catatan penggunaan**
        - Nilai disalin dari tampilan SIKD dalam Rp juta dan berstatus angka tampilan dibulatkan.
        - Se-Prov adalah agregat wilayah provinsi beserta kabupaten/kotanya, bukan hak/alokasi khusus Pemprov.
        - Data lintas wilayah tidak boleh dibandingkan jika snapshot tidak sebanding.
        - Angka pagu/realisasi tidak cukup untuk merekonstruksi formula alokasi. Estimasi alokasi per daerah belum tersedia.
        - EWS di halaman ini bersifat pemantauan data; tidak mengeluarkan peringatan keterlambatan penyaluran.
        """
    )

st.caption(
    "Prototype analitis · Hasil bukan penetapan alokasi final, audit, prediksi, "
    "atau keputusan penyaluran resmi."
)
