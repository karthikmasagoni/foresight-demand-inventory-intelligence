# FORESIGHT — Executive Readout

## Executive Summary
FORESIGHT is a demand and inventory intelligence solution designed to help operations teams make SKU-level replenishment and inventory decisions.

The completed prototype combines:
- historical sales
- product attributes
- calendar information
- inventory snapshots
- weekly demand forecasting
- inventory risk scoring
- operational action recommendations
- a Streamlit dashboard
- a FastAPI scoring service

## 1. Business Findings
- **Storage** is the strongest category by units sold.
- Demand is **seasonal**, making time-based forecasting important.
- **SKU408** is the highest-revenue SKU in the completed analysis.
- **SKU418** is the lowest-selling SKU in the dead-stock analysis.
- The observed promotion flag produced almost no difference in average sales.

## 2. Forecast Performance
| Measure | Result |
|---|---:|
| Seasonal-naive WAPE | **23.33%** |
| ML WAPE | **18.26%** |
| ML Bias | **-4.58%** |

The ML model improved WAPE by **5.07 percentage points** compared with the seasonal-naive benchmark in the completed evaluation period.

## 3. Inventory Decision Engine
The operational decision engine uses forecast demand together with:
- on-hand inventory
- on-order inventory
- supplier lead time
- forecast demand during lead time
- demand volatility

The current dashboard output includes the action categories:
- **REORDER NOW**
- **MARKDOWN/CLEAR**
- **WATCH/VOLATILE**
- **HEALTHY**

## 4. Current Portfolio Signals
The current prototype identified:
- **500 total SKUs**
- **99 REORDER NOW**
- **39 WATCH/VOLATILE**
- **362 HEALTHY**
- **0 MARKDOWN/CLEAR** under the current prototype overstock rule

The zero markdown count should not be interpreted as proof that no overstock exists. Under the current rule and current data, no SKU crossed the selected overstock threshold.

## 5. Dashboard
The client-facing dashboard provides:
- portfolio KPI cards
- business-impact KPIs
- category filtering
- SKU selection
- 4-week demand forecast
- forecast-vs-actual view
- inventory and risk information
- reorder priorities
- markdown priorities

## 6. API
The FastAPI service provides:
- service health endpoint
- SKU scoring endpoint
- forecast output
- stockout/overstock risk
- recommended action
- invalid-SKU error handling
- interactive API documentation through `/docs`

## 7. Recommendations
### Immediate
- Prioritize the current REORDER NOW list for operations review.
- Monitor the WATCH/VOLATILE list for unstable demand.
- Review high-value products such as SKU408 closely.

### Near term
- Validate the risk thresholds with supply-chain stakeholders.
- Run broader rolling-origin validation before production forecasting.
- Review product/category-specific promotion effects.

### Longer term
- Add stronger calendar features once complete calendar coverage is available.
- Improve automated model retraining and monitoring.
- Integrate the scoring API with operational systems.

## 8. Limitations
- Calendar coverage is limited to 2025.
- Inventory snapshots are limited to 2025.
- The current multi-week recursive forecast becomes less certain farther into the horizon.
- Risk thresholds are prototype rules and should be business-validated.
- The reported WAPE/Bias values come from the completed evaluation setup and should not be treated as guaranteed future accuracy.

## 9. Overall Assessment
The prototype demonstrates a complete end-to-end flow from raw business data to demand forecasting, inventory risk scoring, operational recommendations, dashboard visualization, and API access.

The next priority before full production use is stronger validation of the forecasting backtest and business tuning of the inventory decision thresholds.
