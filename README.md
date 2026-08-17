# FORESIGHT

Demand and Inventory Intelligence System

## 1. Business Problem

FORESIGHT is designed to help operations teams forecast SKU-level demand
and identify inventory risks so they can take actions such as:

- REORDER NOW
- MARKDOWN/CLEAR
- WATCH/VOLATILE
- HEALTHY

## 2. Data Sources

The project uses four datasets:

- `sales_daily.csv`
- `sku_master.xlsx`
- `calendar.xlsx`
- `inventory_snapshots.xlsx`

## 3. Data Preparation

The data workflow includes:

- schema and type inspection
- missing-value checks
- duplicate checks
- sales-value validation
- date conversion
- dataset integration
- weekly SKU-level aggregation

## 4. Exploratory Data Analysis

Key findings from the dataset include:

- Storage is the highest-selling category by units.
- Demand shows a seasonal pattern.
- SKU408 is the top revenue SKU.
- SKU418 is the lowest-selling SKU in the dead-stock analysis.
- Promotion days did not materially increase average units sold in the observed data.

## 5. Forecasting

Weekly SKU-level demand is modeled using:

- lag 1 week
- lag 2 weeks
- lag 4 weeks
- leakage-safe 4-week rolling average

A seasonal-naive baseline is used for comparison.

### Current evaluation results

- Seasonal-naive WAPE: 23.33%
- ML WAPE: 18.26%
- ML Bias: -4.58%

These results come from the evaluation setup used in the project and should not be interpreted as guaranteed future accuracy.

## 6. Inventory Risk Engine

The decision engine combines:

- demand forecast
- on-hand inventory
- on-order inventory
- supplier lead time
- forecast demand during lead time
- demand volatility

Outputs:

- REORDER NOW
- MARKDOWN/CLEAR
- WATCH/VOLATILE
- HEALTHY

## 7. Dashboard

The Streamlit dashboard provides:

- total SKU KPI
- reorder/watch/healthy counts
- business-impact KPIs
- category filtering
- SKU selection
- four-week forecast
- forecast vs actual
- inventory and risk information
- reorder priorities
- markdown priorities

## 8. API

FORESIGHT provides a FastAPI scoring service.

### Endpoints

`GET /`

Returns service status.

`GET /score/{sku_id}`

Returns forecast, stockout risk, overstock risk, and recommended action for a SKU.

Interactive API documentation is available at:

`/docs`

## 9. Project Structure

```text
foresight/
├── app/
│   └── app.py
├── src/
│   ├── __init__.py
│   ├── forecast.py
│   └── risk.py
├── data/
│   ├── raw/
│   ├── foresight_decisions.csv
│   ├── foresight_forecasts.csv
│   └── forecast_actual.csv
├── notebooks/
│   └── 01_data_understanding.ipynb
├── api.py
├── requirements.txt
└── README.md