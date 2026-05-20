import streamlit as st


def apply_custom_css():
    st.markdown(
        """
        <style>
        /* ── base ─────────────────────────────────────────────── */
        .main { background-color: #FAFAF8; }

        .block-container {
            padding-top: 2rem;
            padding-bottom: 4rem;
            max-width: 1200px;
        }

        /* ── typography ───────────────────────────────────────── */
        h1 {
            font-size: 2.8rem !important;
            font-weight: 800 !important;
            letter-spacing: -0.04em;
            color: #12372A;
            line-height: 1.15;
        }

        h2 {
            font-size: 1.4rem !important;
            font-weight: 700 !important;
            color: #12372A;
            letter-spacing: -0.02em;
            margin-top: 1.5rem;
        }

        h3 {
            font-size: 1.05rem !important;
            font-weight: 600 !important;
            color: #12372A;
        }

        p, li { color: #374151; line-height: 1.7; }

        /* ── metric cards ─────────────────────────────────────── */
        div[data-testid="stMetric"] {
            background-color: #FFFFFF;
            border: 1px solid #E6E3DC;
            padding: 1.1rem 1.3rem;
            border-radius: 16px;
            box-shadow: 0 1px 6px rgba(0,0,0,0.04);
            transition: box-shadow 0.2s;
        }

        div[data-testid="stMetric"]:hover {
            box-shadow: 0 4px 16px rgba(18,55,42,0.10);
        }

        div[data-testid="stMetricLabel"] {
            font-size: 0.8rem;
            font-weight: 600;
            color: #5F6F65;
            text-transform: uppercase;
            letter-spacing: 0.04em;
        }

        div[data-testid="stMetricValue"] {
            font-size: 1.65rem;
            font-weight: 750;
            color: #12372A;
        }

        /* ── hero card ────────────────────────────────────────── */
        .hero-card {
            background: linear-gradient(135deg, #0D2B1E 0%, #12372A 50%, #1D9E75 100%);
            color: white;
            padding: 2.2rem 2.4rem;
            border-radius: 24px;
            margin-bottom: 1.8rem;
            box-shadow: 0 8px 32px rgba(18,55,42,0.22);
            position: relative;
            overflow: hidden;
        }

        /* subtle texture overlay */
        .hero-card::before {
            content: "";
            position: absolute;
            top: -60px; right: -60px;
            width: 280px; height: 280px;
            background: rgba(255,255,255,0.04);
            border-radius: 50%;
        }

        .hero-card h1 {
            color: white !important;
            margin-bottom: 0.4rem;
            font-size: 2.4rem !important;
        }

        .hero-card p {
            font-size: 1rem;
            color: #C8EAE0;
            max-width: 720px;
            margin-bottom: 1.2rem;
            line-height: 1.65;
        }

        /* ── section cards ────────────────────────────────────── */
        .section-card {
            background-color: #FFFFFF;
            border: 1px solid #E6E3DC;
            padding: 1.4rem 1.6rem;
            border-radius: 18px;
            box-shadow: 0 1px 6px rgba(0,0,0,0.04);
            margin-bottom: 1rem;
            transition: box-shadow 0.2s;
        }

        .section-card:hover {
            box-shadow: 0 4px 18px rgba(18,55,42,0.09);
        }

        /* ── finding card (for key insights) ─────────────────── */
        .finding-card {
            background: linear-gradient(135deg, #EAF7F1 0%, #F0FBF7 100%);
            border: 1px solid #B6E8D4;
            border-left: 4px solid #1D9E75;
            padding: 1rem 1.4rem;
            border-radius: 12px;
            margin-bottom: 0.8rem;
        }

        .finding-card .finding-label {
            font-size: 0.75rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.06em;
            color: #1D9E75;
            margin-bottom: 0.25rem;
        }

        .finding-card .finding-text {
            font-size: 0.95rem;
            color: #12372A;
            font-weight: 500;
        }

        /* ── warning finding card ─────────────────────────────── */
        .finding-card-warn {
            background: linear-gradient(135deg, #FEF3EE 0%, #FEF8F5 100%);
            border: 1px solid #F5C4B3;
            border-left: 4px solid #E24B4A;
            padding: 1rem 1.4rem;
            border-radius: 12px;
            margin-bottom: 0.8rem;
        }

        .finding-card-warn .finding-label {
            font-size: 0.75rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.06em;
            color: #E24B4A;
            margin-bottom: 0.25rem;
        }

        .finding-card-warn .finding-text {
            font-size: 0.95rem;
            color: #7A1F1F;
            font-weight: 500;
        }

        /* ── tags ─────────────────────────────────────────────── */
        .tag {
            display: inline-block;
            background-color: rgba(255,255,255,0.15);
            color: #EAF7F1;
            padding: 0.22rem 0.7rem;
            border-radius: 999px;
            font-size: 0.78rem;
            font-weight: 600;
            margin-right: 0.35rem;
            margin-bottom: 0.35rem;
            border: 1px solid rgba(255,255,255,0.2);
            letter-spacing: 0.02em;
        }

        /* ── small muted text ─────────────────────────────────── */
        .small-muted {
            color: #6B7280;
            font-size: 0.9rem;
            line-height: 1.6;
        }

        /* ── divider label ────────────────────────────────────── */
        .section-label {
            font-size: 0.72rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            color: #9CA3AF;
            margin-bottom: 0.8rem;
            margin-top: 0.5rem;
        }

        /* ── dataframe tweaks ─────────────────────────────────── */
        div[data-testid="stDataFrame"] {
            border-radius: 12px;
            overflow: hidden;
            border: 1px solid #E6E3DC;
        }

        /* ── sidebar ──────────────────────────────────────────── */
        section[data-testid="stSidebar"] {
            background-color: #F4F6F3;
            border-right: 1px solid #E6E3DC;
        }

        section[data-testid="stSidebar"] .block-container {
            padding-top: 1.5rem;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def hero(title: str, subtitle: str):
    st.markdown(
        f"""
        <div class="hero-card">
            <h1>{title}</h1>
            <p>{subtitle}</p>
            <span class="tag">Critical minerals</span>
            <span class="tag">Supply chain risk</span>
            <span class="tag">Energy transition</span>
            <span class="tag">Scenario simulation</span>
            <span class="tag">HHI analysis</span>
        </div>
        """,
        unsafe_allow_html=True,
    )


def finding_card(label: str, text: str, warn: bool = False):
    """
    Render a highlighted insight card.

    Parameters
    ----------
    label : str   Short label shown above the text, e.g. "Key finding"
    text  : str   The insight text.
    warn  : bool  If True, renders in red/warning style. Default is green.

    Usage
    -----
    finding_card("Key finding", "Graphite processing HHI is 8,150 — extreme concentration.")
    finding_card("Risk alert", "DRC supplies 70% of cobalt mining.", warn=True)
    """
    css_class = "finding-card-warn" if warn else "finding-card"
    st.markdown(
        f"""
        <div class="{css_class}">
            <div class="finding-label">{label}</div>
            <div class="finding-text">{text}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def section_label(text: str):
    """Render a small uppercase section divider label."""
    st.markdown(f'<div class="section-label">{text}</div>', unsafe_allow_html=True)
