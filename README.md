# ⛓ CriticalChain

**A supply chain resilience platform for battery-critical minerals.**

CriticalChain maps production concentration, identifies geopolitical chokepoints, and simulates supply disruptions for five minerals central to EVs, batteries, grid storage, and clean-energy infrastructure.

[![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python&logoColor=white)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.35-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-MVP%20Live-brightgreen)]()

> **Live demo → [criticalchain.streamlit.app](https://giorgi-svanidze-criticalchain-appstreamlit-app-qgpwfw.streamlit.app/)**

---

## Screenshots

### Home dashboard
![CriticalChain home dashboard](assets/screenshots/home.png)

### Scenario simulator
![CriticalChain scenario simulator](assets/screenshots/scenario_simulator.png)



---

## The problem

Battery supply chains are dangerously concentrated. A single country controls the majority of processing capacity for most critical minerals — yet most tools that communicate this risk are static reports, not interactive decision-support.

CriticalChain turns fragmented public data into a live, queryable platform.

---

## Key findings (2022 data)

| Material | Stage | HHI | Level | Top country | Share |
|---|---|---|---|---|---|
| Manganese | Processing | 8,742 | 🔴 Extreme | China | 93% |
| Graphite | Processing | 8,150 | 🔴 Extreme | China | 90% |
| Cobalt | Processing | 5,684 | 🔴 Extreme | China | 74% |
| Cobalt | Mining | 5,041 | 🔴 Extreme | DRC | 70% |
| Lithium | Processing | 4,472 | 🟠 High | China | 65% |
| Graphite | Mining | 4,356 | 🟠 High | China | 65% |
| Nickel | Mining | 1,979 | 🟡 Moderate | Indonesia | 37% |

> Graphite processing and manganese processing both exceed HHI 8,000 — eight times the "moderate concentration" threshold used by the IEA. These represent the most acute single-point-of-failure risks in the EV battery supply chain.

---

## Features

### 📊 Overview
Compare HHI concentration scores and top chokepoints across all five materials at a glance.

### 🔍 Material Explorer  
Drill into any material. See country-level production shares, HHI gauges, governance-adjusted risk scores, and a side-by-side mining vs. processing comparison.

### ⚡ Scenario Simulator
Select a disruption — country, material, stage, and severity. The model instantly estimates disrupted global supply share, remaining supply, and top alternative suppliers. Example: *DRC cobalt mining disrupted at 80% severity → 56% of global cobalt mining supply exposed.*

### 🌐 Network Graph
Visualize each mineral's supply chain as a node-edge network. Node size reflects production share. Identifies structural concentration patterns at a glance.

### 📖 Methodology
Full documentation of formulas, data sources, assumptions, and limitations — written for a technical audience.

---

## App pages

```
Home            →  Project overview and dataset preview
Overview        →  HHI comparison across all materials and stages
Material Explorer → Per-material deep dive with risk scoring
Scenario Simulator → Interactive disruption impact calculator
Network Graph   →  Supply chain network visualization
Methodology     →  Formulas, sources, assumptions, limitations
```

---

## Run locally

```bash
git clone https://github.com/YOUR_USERNAME/criticalchain
cd criticalchain
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
streamlit run app/streamlit_app.py
```

Open **http://localhost:8501**

**Requirements:** Python 3.9+

---

## Project structure

```
criticalchain/
│
├── data/
│   ├── starter_data.csv          ← manually curated MVP dataset (USGS / IEA / WGI)
│   ├── raw/                      ← source files
│   └── processed/                ← cleaned outputs
│
├── src/
│   ├── metrics.py                ← HHI calculation, risk scoring, chokepoint ranking
│   ├── scenario_engine.py        ← disruption simulation logic
│   └── ui.py                     ← shared CSS, hero component, finding cards
│
├── app/
│   ├── streamlit_app.py          ← home page
│   └── pages/
│       ├── 1_overview.py
│       ├── 2_material_explorer.py
│       ├── 3_scenario_simulator.py
│       ├── 4_methodology.py
│       └── 5_network_graph.py
│
├── notebooks/
│   └── 01_exploration.ipynb      ← EDA and model development
│
├── requirements.txt
├── .streamlit/config.toml
└── README.md
```

---

## Methodology

### HHI concentration score

The Herfindahl-Hirschman Index measures market concentration as the sum of squared production shares:

```
HHI = Σ (s_i)²
```

where `s_i` is each country's share as a percentage (0–100). Range: 0–10,000. Rows labelled "Other" are excluded to avoid aggregation bias.

**Thresholds (aligned with IEA Critical Minerals Market Review 2023):**

| HHI | Level |
|---|---|
| < 1,500 | 🟢 Low |
| 1,500 – 2,500 | 🟡 Moderate |
| 2,500 – 5,000 | 🟠 High |
| > 5,000 | 🔴 Extreme |

### Governance risk normalization

World Bank WGI political stability scores (−2.5 to +2.5) are normalized to a [0, 1] risk scale:

```
governance_risk = (2.5 - governance_score) / 5
```

Higher value = higher political/institutional risk.

### Chokepoint score

```
chokepoint_score = 0.70 × supply_share_decimal + 0.30 × governance_risk
```

Combines how much supply a country controls with how politically exposed it is. Designed as a transparent screening metric, not a forecasting model.

### Disruption simulation

```
disrupted_supply (%) = country_share (%) × severity (0–1)
remaining_supply (%) = 100 − disrupted_supply (%)
```

Linear first-pass model. Does not yet model price elasticity, inventory buffers, or alternative supplier ramp-up time — noted as planned extensions.

---

## Data sources

| Source | Used for |
|---|---|
| [USGS Mineral Commodity Summaries 2023](https://www.usgs.gov/centers/national-minerals-information-center/mineral-commodity-summaries) | Mining production shares by country |
| [IEA Critical Minerals Market Review 2023](https://www.iea.org/reports/critical-minerals-market-review-2023) | Processing shares and concentration benchmarks |
| [World Bank WGI 2022](https://info.worldbank.org/governance/wgi/) | Political stability / governance scores |

---

## Limitations

The MVP is intentionally simplified. It does **not** model:
- Inventory buffers or strategic reserves
- Substitution limits between suppliers  
- Ramp-up time for alternative production
- Price elasticity or demand response
- Bilateral trade flow routing
- Recycling or secondary supply

---

## Roadmap

- [ ] UN Comtrade bilateral trade flow data (v2)
- [ ] NetworkX graph with betweenness centrality
- [ ] Multi-year trend analysis (2018–2023)
- [ ] Price impact estimation via published elasticities
- [ ] Expanded material coverage (REEs, silicon, platinum group)
- [ ] Validation against IEA, DOE criticality assessments

---

## About

Built by **Giorgi Svanidze (https://linkedin.com/in/giorgisvanidze)** — Chemical Engineering and Supply Chain Management student with research interests in supply chain analytics, energy systems, and critical materials strategy.

This project sits at the intersection of chemical engineering, supply chain risk analysis, and energy transition strategy.

---

## Tech stack

`Python` · `Pandas` · `NumPy` · `Plotly` · `Streamlit` · `NetworkX`

---

*Data current as of 2022. Built for portfolio and research purposes — not investment or policy advice.*
