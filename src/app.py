"""Streamlit UI prototype for DBH SDA Perikanan scenario comparison."""

import json
from decimal import Decimal
from pathlib import Path

import streamlit as st

from engine.calculations import calculate_metrics, compare_scenarios


DATA_PATH = Path(__file__).parent / "data" / "observations.json"


def load_observations() -> list[dict]:
    with DATA_PATH.open(encoding="utf-8") as data_file:
        return json.load(data_file)


def fmt_billion(value: Decimal) -> str:
    return f"Rp{value:,.2f} miliar".replace(",", "_").replace(".", ",").replace("_", ".")


def fmt_ratio(value: Decimal | None) -> str:
    return "Tidak dapat dihitung" if value is None else f"{value:.2f}%".replace(".", ",")


def fmt_signed_billion(value: Decimal) -> str:
    prefix = "+" if value > 0 else ""
    return f"{prefix}{fmt_billion(value)}"


st.set_page_config(
    page_title="DBH Perikanan | EWS + DSS Prototype",
    page_icon="🐟",
    layout="wide",
)

st.markdown(
    """
    <style>
    .stApp { background: #f5f7fb; }
    .block-container { padding-top: 2rem; max-width: 1200px; }
    .hero { padding: 1.5rem 1.7rem; border-radius: 18px; background: #102a43; color: white; margin-bottom: 1.2rem; }
    .hero p { color: #d9e2ec; margin-bottom: .2rem; }
    .eyebrow { text-transform: uppercase; letter-spacing: .12em; color: #8fe3cf !important; font-size: .75rem; font-weight: 700; }
    .small-note { color: #52606d; font-size: .88rem; }
    div[data-testid="stMetric"] { background: white; padding: 1rem; border: 1px solid #d9e2ec; border-radius: 12px; }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="hero">
      <p class="eyebrow">Early Warning + Decision Support • Prototype</p>
      <h1 style="color:white; margin:.2rem 0">DBH SDA Perikanan</h1>
      <p>Bandingkan pagu, realisasi, dan dampak asumsi skenario untuk TA 2024.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

observations = load_observations()
by_name = {item["region_name"]: item for item in observations}
region = st.selectbox("Wilayah", list(by_name.keys()), index=0)
observation = by_name[region]

left, right = st.columns([1, 1.35], gap="large")

with left:
    st.subheader("Data dasar")
    st.caption(f"{observation['fund_type']} · TA {observation['fiscal_year']} · {observation['region_level']}")

    if observation["value_status"] != "available":
        st.warning("Nilai untuk wilayah ini belum terverifikasi. Status ini bukan nilai nol.")
        st.write(observation["source_note"])
        st.link_button("Buka sumber kandidat", observation["source_url"])
        st.info("Input dan perhitungan dinonaktifkan sampai angka resmi diperiksa.")
        st.stop()

    baseline_budget = Decimal(observation["budget_billion_display"])
    baseline_realization = Decimal(observation["realization_billion_display"])

    st.metric("Pagu sumber", fmt_billion(baseline_budget))
    st.metric("Realisasi sumber", fmt_billion(baseline_realization))
    st.caption(
        f"Status: {observation['precision_status']} · snapshot {observation['source_as_of']}"
    )

    with st.expander("Lihat sumber dan batasan"):
        st.write(observation["source_title"])
        st.write(observation["source_note"])
        st.link_button("Buka sumber data", observation["source_url"])

with right:
    st.subheader("Skenario alternatif")
    st.caption("Ubah input untuk simulasi. Nilai skenario bukan realisasi resmi atau ramalan.")
    scenario_budget_input = st.number_input(
        "Pagu skenario (miliar rupiah)",
        min_value=0.0,
        value=float(baseline_budget),
        step=0.01,
        format="%.2f",
        key=f"budget-{observation['id']}",
    )
    scenario_realization_input = st.number_input(
        "Realisasi skenario (miliar rupiah)",
        min_value=0.0,
        value=float(baseline_realization),
        step=0.01,
        format="%.2f",
        key=f"realization-{observation['id']}",
    )
    assumption_note = st.text_input(
        "Catatan asumsi skenario",
        value="Simulasi untuk melihat sensitivitas hasil.",
        key=f"note-{observation['id']}",
    )

    scenario_budget = Decimal(str(scenario_budget_input))
    scenario_realization = Decimal(str(scenario_realization_input))
    baseline_result = calculate_metrics(baseline_budget, baseline_realization)
    scenario_result = calculate_metrics(scenario_budget, scenario_realization)
    comparison = compare_scenarios(
        baseline_budget,
        baseline_realization,
        scenario_budget,
        scenario_realization,
    )

    st.markdown("#### Perbandingan hasil")
    col_a, col_b, col_c = st.columns(3)
    col_a.metric(
        "Rasio baseline",
        fmt_ratio(baseline_result["ratio_pct"]),
    )
    col_b.metric(
        "Rasio skenario",
        fmt_ratio(scenario_result["ratio_pct"]),
        delta=(
            None
            if comparison["ratio_delta_pct_points"] is None
            else f"{comparison['ratio_delta_pct_points']:+.2f} poin persentase"
        ),
    )
    col_c.metric("Sisa pagu skenario", fmt_billion(scenario_result["gap"]))

    st.write(
        "**Perubahan terhadap baseline:** "
        f"pagu {fmt_signed_billion(comparison['budget_delta'])}; "
        f"realisasi {fmt_signed_billion(comparison['realization_delta'])}."
    )
    st.write(f"**Catatan asumsi:** {assumption_note or 'Belum diisi.'}")

    signal = scenario_result["signal"]
    if signal == "MONITOR_GAP":
        st.warning("Sinyal demo: ada selisih pagu–realisasi pada angka skenario.")
    elif signal == "REVIEW_OVER_BUDGET":
        st.warning("Sinyal demo: realisasi skenario melebihi pagu; periksa basis dan sumber.")
    else:
        st.success("Pada angka tampilan, tidak terlihat selisih pagu–realisasi.")
    st.caption(f"Rule: {signal} · advisory · membutuhkan tinjauan manusia")

st.divider()
st.markdown(
    "**Batas interpretasi:** angka sumber SIKD untuk contoh ini dibulatkan dalam miliar rupiah. "
    "Data tahunan tidak menunjukkan jadwal penyaluran, sehingga UI ini tidak menyimpulkan keterlambatan. "
    "Sinyal adalah aturan demo, bukan ambang risiko atau keputusan resmi."
)
