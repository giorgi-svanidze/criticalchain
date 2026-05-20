import sys
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT))

from src.ui import apply_custom_css

st.set_page_config(
    page_title="CriticalChain | Network Graph",
    page_icon="⛓",
    layout="wide",
)

apply_custom_css()

st.title("Network Graph")
st.subheader("Visualize critical mineral supply concentration as a country-stage network")

st.markdown(
    """
    This page visualizes each mineral's simplified supply chain as a network:
    material → supply chain stage → country. Larger country nodes represent higher
    production or processing share.
    """
)

@st.cache_data
def load_data():
    return pd.read_csv(ROOT / "data" / "starter_data.csv")

df = load_data()

material = st.selectbox(
    "Select material",
    sorted(df["material"].unique()),
)

material_df = df[df["material"] == material].copy()

st.markdown("---")

# Build simple node positions manually
nodes = []
edges = []

# central material node
nodes.append({
    "name": material,
    "type": "Material",
    "x": 0,
    "y": 0,
    "size": 35,
    "label": material,
})

stage_positions = {
    "Mining": (-1.5, 0.8),
    "Processing": (1.5, 0.8),
}

for stage, (x, y) in stage_positions.items():
    nodes.append({
        "name": stage,
        "type": "Stage",
        "x": x,
        "y": y,
        "size": 25,
        "label": stage,
    })
    edges.append((material, stage, 1))

for stage in ["Mining", "Processing"]:
    stage_df = material_df[material_df["stage"] == stage].sort_values(
        "production_share_pct",
        ascending=False,
    )

    if stage == "Mining":
        base_x = -1.5
    else:
        base_x = 1.5

    for i, row in enumerate(stage_df.itertuples()):
        y = -0.2 - i * 0.45
        country_node = f"{row.country} ({stage})"

        nodes.append({
            "name": country_node,
            "type": "Country",
            "x": base_x,
            "y": y,
            "size": 10 + row.production_share_pct * 0.45,
            "label": f"{row.country}<br>{row.production_share_pct:.0f}%",
        })

        edges.append((stage, country_node, row.production_share_pct))

node_df = pd.DataFrame(nodes)

# Build edge traces
edge_x = []
edge_y = []

for source, target, weight in edges:
    source_node = node_df[node_df["name"] == source].iloc[0]
    target_node = node_df[node_df["name"] == target].iloc[0]

    edge_x += [source_node["x"], target_node["x"], None]
    edge_y += [source_node["y"], target_node["y"], None]

edge_trace = go.Scatter(
    x=edge_x,
    y=edge_y,
    line=dict(width=1.5),
    hoverinfo="none",
    mode="lines",
)

node_trace = go.Scatter(
    x=node_df["x"],
    y=node_df["y"],
    mode="markers+text",
    text=node_df["label"],
    textposition="top center",
    marker=dict(
        size=node_df["size"],
        line=dict(width=1),
    ),
    hovertemplate=(
        "<b>%{text}</b><br>"
        "Node type: %{customdata}<extra></extra>"
    ),
    customdata=node_df["type"],
)

fig = go.Figure(data=[edge_trace, node_trace])

fig.update_layout(
    title=f"{material} simplified supply-chain concentration network",
    showlegend=False,
    height=700,
    margin=dict(l=20, r=20, t=60, b=20),
    xaxis=dict(showgrid=False, zeroline=False, visible=False),
    yaxis=dict(showgrid=False, zeroline=False, visible=False),
)

st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

st.subheader("Network interpretation")

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

col1, col2 = st.columns(2)

col1.metric(
    "Largest mining node",
    f"{top_mining['country']} ({top_mining['production_share_pct']:.0f}%)",
)

col2.metric(
    "Largest processing node",
    f"{top_processing['country']} ({top_processing['production_share_pct']:.0f}%)",
)

st.caption(
    "This is a simplified visual network for portfolio demonstration. Future versions can use NetworkX with bilateral trade-flow data."
)
