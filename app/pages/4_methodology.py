import streamlit as st

from src.ui import apply_custom_css


st.set_page_config(
    page_title="CriticalChain | Methodology",
    page_icon="⛓",
    layout="wide",
)

apply_custom_css()

st.title("Methodology")
st.subheader("How CriticalChain estimates concentration and disruption risk")

st.markdown("""
CriticalChain is an open-source portfolio project that explores supply chain
resilience for battery-critical minerals.

The current MVP focuses on five materials:

- Lithium
- Cobalt
- Nickel
- Manganese
- Graphite

For each material, the app separates the supply chain into two simplified stages:

1. **Mining** — where raw mineral production is concentrated
2. **Processing** — where refining or processing capacity is concentrated

The goal is not to make precise investment or policy forecasts. Instead, the MVP
demonstrates a transparent decision-support framework for identifying potential
supply chokepoints.
""")

st.markdown("---")

st.header("Data sources")

st.markdown("""
The starter dataset is manually curated from public critical minerals sources:

- **USGS Mineral Commodity Summaries 2023** for mining / production concentration
- **IEA Critical Minerals Market Review 2023** for processing concentration
- **World Bank Worldwide Governance Indicators 2022** for political stability / governance scores

The MVP uses a small curated dataset so the first version remains transparent,
reproducible, and easy to inspect.
""")

st.markdown("---")

st.header("HHI concentration score")

st.markdown("""
The Herfindahl-Hirschman Index, or HHI, is used to estimate supply concentration.

HHI is calculated as:

`HHI = sum(s_i²)`

where `s_i` is each country's supply share expressed as a percentage.

Examples:

- A monopoly supplier with 100% share has HHI = 10,000
- Two equal suppliers with 50% each have HHI = 5,000
- Ten equal suppliers with 10% each have HHI = 1,000

This project uses common screening thresholds:

- **HHI < 1,500**: lower concentration
- **1,500 ≤ HHI < 2,500**: moderate concentration
- **HHI ≥ 2,500**: high concentration
""")

st.markdown("---")

st.header("Governance risk")

st.markdown("""
The governance score comes from the World Bank Worldwide Governance Indicators
political stability measure.

The original score ranges approximately from:

- **-2.5** = less stable
- **+2.5** = more stable

CriticalChain converts this into a normalized risk score between 0 and 1:

`governance_risk = (2.5 - governance_score) / 5`

A higher governance risk means a country is treated as more exposed to political
or institutional disruption risk.
""")

st.markdown("---")

st.header("Chokepoint score")

st.markdown("""
The current MVP uses a simple transparent chokepoint score:

`chokepoint_score = 0.70 × supply_share + 0.30 × governance_risk`

where:

- `supply_share` is expressed as a decimal, such as 0.70 for 70%
- `governance_risk` ranges from 0 to 1

This is not a final risk model. It is a first-pass screening metric designed to
highlight countries that combine large supply share with elevated governance risk.
""")

st.markdown("---")

st.header("Scenario simulator")

st.markdown("""
The scenario simulator estimates the direct supply exposure from a country-level
disruption.

The MVP formula is:

`disrupted_global_supply = country_supply_share × disruption_severity`

Example:

If the DRC accounts for 70% of cobalt mining and a disruption removes 80% of
that supply:

`70% × 80% = 56%`

So the app estimates that 56% of global cobalt mining supply is exposed in that
scenario.
""")

st.markdown("---")

st.header("Current limitations")

st.markdown("""
The current version is intentionally simplified. It does **not yet** model:

- inventories or strategic reserves
- substitution limits between suppliers
- ramp-up time for alternative production
- price elasticity
- demand destruction
- downstream manufacturer-specific exposure
- bilateral trade routes
- recycling supply
- environmental permitting delays

These are planned extensions for future versions.
""")

st.markdown("---")

st.header("Planned next steps")

st.markdown("""
Future versions will add:

1. Network graphs using NetworkX
2. UN Comtrade bilateral trade-flow data
3. More materials, including rare earth elements and silicon
4. Scenario types such as export bans, mine closures, and trade restrictions
5. Sensitivity analysis for chokepoint-score weights
6. Validation against IEA, USGS, and DOE criticality assessments
""")
