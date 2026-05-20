import sys
from pathlib import Path

import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

from src.ui import apply_custom_css, hero

st.set_page_config(
    page_title="CriticalChain",
    page_icon="⛓",
    layout="wide",
    initial_sidebar_state="expanded",
)

apply_custom_css()

hero(
    "CriticalChain",
    "A supply chain resilience simulator for battery-critical minerals. "
    "Explore concentration risk, identify chokepoint countries, and test disruption scenarios across lithium, cobalt, nickel, manganese, and graphite."
)

@st.cache_data
def load_data():
    return pd.read_csv(ROOT / "data" / "starter_data.csv")

df = load_data()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Materials", df["material"].nunique())
col2.metric("Countries", df["country"].nunique())
col3.metric("Stages", df["stage"].nunique())
col4.metric("Rows", len(df))

st.markdown("")

left, right = st.columns([1.1, 0.9])

with left:
    st.markdown(
        """
        <div class="section-card">
        <h3>What this project does</h3>
        <p class="small-muted">
        CriticalChain turns fragmented public data on critical minerals into a simple decision-support tool.
        It calculates concentration risk, ranks country chokepoints, and estimates direct supply exposure
        under disruption scenarios.
        </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="section-card">
        <h3>Why it matters</h3>
        <p class="small-muted">
        Battery supply chains are highly concentrated. A disruption in one country can affect clean-energy,
        EV, battery, defense, and manufacturing supply chains. This tool demonstrates how graph and risk
        analytics can support strategic resilience planning.
        </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with right:
    st.markdown(
        """
        <div class="section-card">
        <h3>Navigate the app</h3>
        <p><b>Overview</b><br><span class="small-muted">Compare HHI and chokepoint risk across materials.</span></p>
        <p><b>Material Explorer</b><br><span class="small-muted">Inspect mining and processing concentration by country.</span></p>
        <p><b>Scenario Simulator</b><br><span class="small-muted">Estimate supply exposure under country-level disruptions.</span></p>
        <p><b>Methodology</b><br><span class="small-muted">Review formulas, assumptions, limitations, and data sources.</span></p>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("---")
st.subheader("Starter dataset preview")
st.dataframe(df, use_container_width=True, hide_index=True)
