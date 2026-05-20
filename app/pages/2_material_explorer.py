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
    page_title="CriticalChain | Material Explorer",
    page_icon="⛓",
    layout="wide",
)

apply_custom_css()

st.title("Material Explorer")
st.subheader("Explore concentration risk by material and supply chain stage")

@st.cache_data
def load_data():
    return pd.read_csv(ROOT / "data" / "starter_data.csv")

df = load_data()
df_scored = add_risk_scores(df)
hhi_df = calculate_hhi(df)

materials = sorted(df["material"].unique())
selected_material = st.selectbox("Select a material", materials)

material_df = df_scored[df_scored["material"] == selected_material].copy()
material_hhi = hhi_df[hhi_df["material"] == selected_material].copy()
material_hhi["risk_category"] = material_hhi["hhi"].apply(classify_hhi)

st.markdown("---")

col1, col2, col3 = st.columns(3)

top_mining = (
    material_df[material_df["stage"] == "Mining"]
    .sort_values("production_share_pct", ascending=False)
    .iloc[0]
)

top_processing = (
    material_df[material_df["stage"] == "Processing"]
    .sort_values("production_share_pct", ascending=False)
    .iloc[0]
)

highest_stage_hhi = material_hhi.sort_values("hhi", ascending=False).iloc[0]

col1.metric(
    "Top mining country",
    f"{top_mining['country']} ({top_mining['production_share_pct']:.0f}%)"
)

col2.metric(
    "Top processing country",
    f"{top_processing['country']} ({top_processing['production_share_pct']:.0f}%)"
)

col3.metric(
    "Highest concentration stage",
    f"{highest_stage_hhi['stage']} ({highest_stage_hhi['hhi']:,.0f})"
)

st.markdown("---")

st.subheader(f"{selected_material}: supply share by country")

fig = px.bar(
    material_df.sort_values(["stage", "production_share_pct"], ascending=[True, False]),
    x="country",
    y="production_share_pct",
    color="stage",
    barmode="group",
    text="production_share_pct",
    labels={
        "country": "Country",
        "production_share_pct": "Production / processing share (%)",
        "stage": "Stage",
    },
)

fig.update_traces(texttemplate="%{text:.0f}%", textposition="outside")
fig.update_layout(yaxis_range=[0, 100])

st.plotly_chart(fig, use_container_width=True)

st.subheader("HHI concentration by stage")

hhi_fig = px.bar(
    material_hhi,
    x="stage",
    y="hhi",
    text="risk_category",
    labels={
        "stage": "Stage",
        "hhi": "HHI concentration score",
    },
)

hhi_fig.add_hline(y=2500, line_dash="dash", annotation_text="High concentration threshold")
hhi_fig.add_hline(y=1500, line_dash="dot", annotation_text="Moderate concentration threshold")

st.plotly_chart(hhi_fig, use_container_width=True)

st.subheader("Country-level risk table")

risk_table = material_df[
    [
        "material",
        "stage",
        "country",
        "production_share_pct",
        "governance_score",
        "governance_risk",
        "chokepoint_score",
        "notes",
    ]
].sort_values("chokepoint_score", ascending=False)

st.dataframe(risk_table, use_container_width=True)

st.caption(
    "Higher chokepoint scores indicate countries that combine large supply share with higher political/governance risk."
)
