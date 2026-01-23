import pandas as pd
from pathlib import Path

# Load CSV files
BASE_DIR = Path(__file__).resolve().parent.parent

gi_df = pd.read_csv(BASE_DIR / "data/nutrition_db/gi_table.csv")
carb_df = pd.read_csv(BASE_DIR / "data/nutrition_db/carbs_table.csv")

def get_gi(food_name: str):
    """
    Returns GI value for given food.
    """
    row = gi_df[gi_df["food"] == food_name]
    if row.empty:
        return None
    return float(row["gi"].values[0])

def get_carbs_per_100g(food_name: str):
    """
    Returns carbs per 100g for given food.
    """
    row = carb_df[carb_df["food"] == food_name]
    if row.empty:
        return None
    return float(row["carbs_per_100g"].values[0])
