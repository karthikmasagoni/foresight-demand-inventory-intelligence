from fastapi import FastAPI, HTTPException
import pandas as pd
from pathlib import Path

app = FastAPI(
    title="FORESIGHT Scoring API",
    version="1.0.0"
)

BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "data" / "foresight_decisions.csv"

data = pd.read_csv(DATA_FILE)


@app.get("/")
def home():
    return {
        "service": "FORESIGHT",
        "status": "running"
    }


@app.get("/score/{sku_id}")
def score_sku(sku_id: str):

    result = data[
        data["sku_id"].astype(str) == str(sku_id)
    ]

    if result.empty:
        raise HTTPException(
            status_code=404,
            detail=f"SKU '{sku_id}' not found"
        )

    row = result.iloc[0]

    return {
        "sku_id": sku_id,
        "forecast_week_1": float(row["forecast_week_1"]),
        "forecast_week_2": float(row["forecast_week_2"]),
        "forecast_week_3": float(row["forecast_week_3"]),
        "forecast_week_4": float(row["forecast_week_4"]),
        "stockout_risk": str(row["stockout_risk"]),
        "overstock_risk": str(row["overstock_risk"]),
        "action": str(row["action"])
    }