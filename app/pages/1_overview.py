import sys
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT))

from src.metrics import calculate_hhi, classify_hhi, add_risk_scores
from src.ui import apply_custom_css


st.set_page_config(
    page_title="CriticalChain | Overview",
    page_icon="⛓",
    layout="wide",
)

apply_custom_css()

st.title("Overview")
st.subheader("Supply concentration and chokepoint risk across battery-critical minerals")

@st.cache_data
def load_data():
    return pd.read_csv(ROOT / "data" / "starter_data.csv")

df = load_data()
df_scored = add_risk_scores(df)
hhi_df = calculate_hhi(df)

hhi_df["risk_category"] = hhi_df["hhi"].apply(classify_hhi)

highest_hhi_row = hhi_df.sort_values("hhi", ascending=False).iloc[0]
highest_risk_row = df_scored.sort_values("chokepoint_score", ascending=False).iloc[0]

col1, col2, col3, col4 = st.columns(4)

col1.metric("Materials tracked", df["material"].nunique())
col2.metric("Highest concentration", f"{highest_hhi_row['material']} / {highest_hhi_row['stage']}")
col3.metric("Highest HHI", f"{highest_hhi_row['hhi']:,.0f}")
col4.metric("Top chokepoint", f"{highest_risk_row['country']}")

st.markdown("---")

st.subheader("HHI concentration by material and stage")

fig = px.bar(
    hhi_df.sort_values("hhi", ascending=False),
    x="material",
    y="hhi",
    color="stage",
    barmode="group",
    text="risk_category",
    labels={
        "material": "Material",
        "hhi": "HHI concentration score",
        "stage": "Supply chain stage",
    },
)

fig.add_hline(y=2500, line_dash="dash", annotation_text="High concentration threshold")
fig.add_hline(y=1500, line_dash="dot", annotation_text="Moderate concentration threshold")

st.plotly_chart(fig, use_container_width=True)

st.subheader("Top country chokepoints")

top_chokepoints = (
    df_scored.sort_values("chokepoint_score", ascending=False)
    [["material", "stage", "country", "production_share_pct", "governance_score", "governance_risk", "chokepoint_score"]]
    .head(15)
)

st.dataframe(top_chokepoints, use_container_width=True)

st.caption(
    "Chokepoint score is a first-pass composite metric combining supply share and governance risk. "
    "It is intended for screening, not investment or policy decisions."
)
