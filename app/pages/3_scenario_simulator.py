import sys
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT))

from src.scenario_engine import simulate_disruption, classify_disruption
from src.ui import apply_custom_css


st.set_page_config(
    page_title="CriticalChain | Scenario Simulator",
    page_icon="⛓",
    layout="wide",
)

apply_custom_css()

st.title("Scenario Simulator")
st.subheader("Estimate supply exposure under country-level disruption scenarios")

st.markdown(
    """
    This simulator estimates how much global supply could be affected if a major
    mining or processing country experiences a disruption.

    The model is intentionally transparent: it multiplies the selected country's
    supply share by the disruption severity selected by the user.
    """
)

@st.cache_data
def load_data():
    return pd.read_csv(ROOT / "data" / "starter_data.csv")

df = load_data()

st.markdown("---")

col_a, col_b, col_c = st.columns(3)

with col_a:
    material = st.selectbox(
        "Select material",
        sorted(df["material"].unique()),
    )

material_df = df[df["material"] == material]

with col_b:
    stage = st.selectbox(
        "Select supply chain stage",
        sorted(material_df["stage"].unique()),
    )

stage_df = material_df[material_df["stage"] == stage].sort_values(
    "production_share_pct",
    ascending=False,
)

with col_c:
    country = st.selectbox(
        "Select disrupted country",
        stage_df["country"].tolist(),
    )

severity_pct = st.slider(
    "Disruption severity",
    min_value=0,
    max_value=100,
    value=80,
    step=5,
    help="Example: 80% means 80% of the selected country's supply is unavailable.",
)

result = simulate_disruption(
    df=df,
    material=material,
    stage=stage,
    country=country,
    severity_pct=severity_pct,
)

risk_level = classify_disruption(result["disrupted_global_share"])

st.markdown("---")

metric1, metric2, metric3, metric4 = st.columns(4)

metric1.metric(
    "Selected country share",
    f"{result['country_share']:.1f}%",
)

metric2.metric(
    "Disrupted global supply",
    f"{result['disrupted_global_share']:.1f}%",
)

metric3.metric(
    "Remaining global supply",
    f"{result['remaining_global_supply']:.1f}%",
)

metric4.metric(
    "Scenario severity",
    risk_level,
)

st.markdown("---")

st.subheader("Scenario interpretation")

if risk_level == "Severe":
    st.error(
        f"A {severity_pct}% disruption in {country}'s {material} {stage.lower()} supply "
        f"could affect approximately {result['disrupted_global_share']:.1f}% of global supply. "
        "This represents a severe chokepoint scenario in this simplified model."
    )
elif risk_level == "High":
    st.warning(
        f"This scenario affects approximately {result['disrupted_global_share']:.1f}% of global supply. "
        "This is a high-exposure disruption and would likely require rapid substitution or demand management."
    )
elif risk_level == "Moderate":
    st.info(
        f"This scenario affects approximately {result['disrupted_global_share']:.1f}% of global supply. "
        "This is a moderate disruption that may be manageable with alternative suppliers."
    )
else:
    st.success(
        f"This scenario affects approximately {result['disrupted_global_share']:.1f}% of global supply. "
        "This is a relatively low-exposure disruption in this simplified model."
    )

st.subheader("Supply before and after disruption")

before_after = pd.DataFrame({
    "Category": ["Available supply", "Disrupted supply"],
    "Share": [
        result["remaining_global_supply"],
        result["disrupted_global_share"],
    ],
})

fig = go.Figure(
    data=[
        go.Pie(
            labels=before_after["Category"],
            values=before_after["Share"],
            hole=0.55,
        )
    ]
)

fig.update_layout(
    title=f"{material} {stage}: supply exposure under {country} disruption",
)

st.plotly_chart(fig, use_container_width=True)

st.subheader("Top alternative suppliers")

st.dataframe(result["alternatives"], use_container_width=True)

st.caption(
    "This MVP does not yet model ramp-up time, price elasticity, inventory buffers, or substitution limits. "
    "Those are planned extensions for the polished version."
)
