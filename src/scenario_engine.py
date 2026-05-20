import pandas as pd


def simulate_disruption(
    df: pd.DataFrame,
    material: str,
    stage: str,
    country: str,
    severity_pct: float,
) -> dict:
    """
    Simulate the impact of a disruption to one country for one material and stage.

    Parameters
    ----------
    df : pd.DataFrame
        Starter dataset.
    material : str
        Selected mineral, e.g. Cobalt.
    stage : str
        Mining or Processing.
    country : str
        Country being disrupted.
    severity_pct : float
        Percent of that country's supply disrupted, from 0 to 100.

    Returns
    -------
    dict
        Summary of disrupted supply and alternative suppliers.
    """
    subset = df[
        (df["material"] == material) &
        (df["stage"] == stage)
    ].copy()

    if subset.empty:
        raise ValueError("No data found for selected material and stage.")

    disrupted = subset[subset["country"] == country]

    if disrupted.empty:
        raise ValueError("Selected country not found for this material and stage.")

    country_share = float(disrupted["production_share_pct"].iloc[0])
    disrupted_global_share = country_share * (severity_pct / 100)

    remaining_global_supply = 100 - disrupted_global_share

    alternatives = (
        subset[subset["country"] != country]
        .sort_values("production_share_pct", ascending=False)
        [["country", "production_share_pct", "governance_score", "notes"]]
        .head(5)
        .reset_index(drop=True)
    )

    return {
        "material": material,
        "stage": stage,
        "country": country,
        "severity_pct": severity_pct,
        "country_share": country_share,
        "disrupted_global_share": disrupted_global_share,
        "remaining_global_supply": remaining_global_supply,
        "alternatives": alternatives,
    }


def classify_disruption(disrupted_global_share: float) -> str:
    """
    Classify disruption severity based on affected global supply share.
    """
    if disrupted_global_share < 5:
        return "Low"
    elif disrupted_global_share < 15:
        return "Moderate"
    elif disrupted_global_share < 30:
        return "High"
    else:
        return "Severe"
