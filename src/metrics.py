import pandas as pd


def calculate_hhi(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate Herfindahl-Hirschman Index (HHI) by material, stage, and year.

    HHI = sum(market_share_i^2)

    If shares are in percentages, HHI ranges from 0 to 10,000.
    Example:
    100% monopoly = 10,000
    50/50 split = 5,000
    10 equal suppliers = 1,000
    """
    hhi = (
        df.groupby(["material", "stage", "year"])["production_share_pct"]
        .apply(lambda x: (x ** 2).sum())
        .reset_index(name="hhi")
    )

    return hhi


def classify_hhi(hhi: float) -> str:
    """
    Classify concentration using common antitrust-style HHI thresholds.
    """
    if hhi < 1500:
        return "Low"
    elif hhi < 2500:
        return "Moderate"
    else:
        return "High"


def normalize_governance_risk(governance_score: float) -> float:
    """
    Convert World Bank governance score into a risk score.

    WGI political stability roughly ranges from -2.5 to +2.5.
    Higher governance_score = more stable.
    Higher output risk = more risky.

    Output is clipped between 0 and 1.
    """
    risk = (2.5 - governance_score) / 5
    return max(0, min(1, risk))


def add_risk_scores(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add country-level risk scores.

    Composite chokepoint score combines:
    - production/processing share
    - governance risk

    This is a first-pass transparent scoring model.
    """
    df = df.copy()

    df["supply_share_decimal"] = df["production_share_pct"] / 100
    df["governance_risk"] = df["governance_score"].apply(normalize_governance_risk)

    df["chokepoint_score"] = (
        0.70 * df["supply_share_decimal"] +
        0.30 * df["governance_risk"]
    )

    return df
