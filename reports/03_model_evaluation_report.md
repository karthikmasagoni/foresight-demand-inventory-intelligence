# FORESIGHT — Forecasting Model Evaluation Report

## 1. Objective
The forecasting component was designed to estimate weekly SKU-level demand and provide a benchmark for inventory decision-making.

## 2. Forecasting Approach
Weekly demand was created at SKU level.

The main forecasting features used were:
- `lag_1`
- `lag_2`
- `lag_4`
- leakage-safe `rolling_4`

A seasonal-naive benchmark was also evaluated.

A Random Forest regression model was used for the machine-learning forecast.

## 3. Evaluation Metrics
The project used WAPE as the primary accuracy metric and also evaluated forecast bias.

### Results from the completed evaluation
| Metric | Result |
|---|---:|
| Seasonal-naive WAPE | **23.33%** |
| ML WAPE | **18.26%** |
| ML Bias | **-4.58%** |

The ML model therefore produced a WAPE that was **5.07 percentage points lower** than the seasonal-naive benchmark in the completed test-period evaluation.

Relative reduction in WAPE is approximately **21.7%**.

## 4. Bias Interpretation
The ML bias of **-4.58%** under the project's `actual - forecast` convention indicates a tendency toward overall over-forecasting in the evaluated period.

This directional behavior should be monitored because persistent over-forecasting can increase inventory exposure.

## 5. Feature Engineering
The feature engineering process used prior demand only for the rolling feature:
- the current week's actual demand was excluded from the rolling calculation through `shift(1)`;
- this reduces the risk of leakage from the target period.

## 6. Important Evaluation Note
The completed numerical results above come from the evaluation setup actually run during the project.

A full production-grade rolling-origin cross-validation with a stored multi-fold summary was not completed in the final workflow. Therefore, the report does **not** claim that these metrics are rolling-cross-validation averages.

## 7. Interpretation
The model outperformed the seasonal-naive benchmark on the evaluated test period. This supports using the ML model as the current prototype forecasting approach.

However, this should not be interpreted as guaranteed future performance. Monitoring, retraining, and additional rolling-origin validation are recommended before production deployment.

## 8. Limitations
- Recursive multi-week forecasts accumulate uncertainty over horizon.
- Calendar and inventory coverage is incomplete for historical periods.
- Model performance may vary across individual SKUs.
- Prototype results should be validated over additional time windows before operational commitment.

## 9. Conclusion
The completed evaluation indicates that the ML forecast improved on the seasonal-naive benchmark for the tested period. The result is promising for the FORESIGHT prototype while still requiring broader validation for production use.
