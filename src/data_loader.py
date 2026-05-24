"""Data loading helpers for the insurance analytics notebooks and scripts."""

from pathlib import Path

import pandas as pd


def load_insurance_data(path: str | Path = "data/raw/insurance_data.csv") -> pd.DataFrame:
    """Load insurance data and parse transaction dates when present."""
    data_path = Path(path)
    if not data_path.exists():
        raise FileNotFoundError(f"Insurance data file not found: {data_path}")

    df = pd.read_csv(data_path)
    if "TransactionMonth" in df.columns:
        df["TransactionMonth"] = pd.to_datetime(df["TransactionMonth"], errors="coerce")
    return df


def add_loss_ratio(df: pd.DataFrame) -> pd.DataFrame:
    """Return a copy of the data with LossRatio = TotalClaims / TotalPremium."""
    required = {"TotalClaims", "TotalPremium"}
    missing = required.difference(df.columns)
    if missing:
        raise KeyError(f"Missing required columns for loss ratio: {sorted(missing)}")

    enriched = df.copy()
    enriched["LossRatio"] = enriched["TotalClaims"] / enriched["TotalPremium"].replace(0, pd.NA)
    return enriched
