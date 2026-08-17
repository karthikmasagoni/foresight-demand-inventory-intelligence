# FORESIGHT — EDA Insight Report

## 1. Purpose
This report summarizes the main exploratory findings identified before forecasting and inventory-risk modeling.

## 2. Demand and Product Findings

### Highest-selling category
**Storage** was the highest-selling category by units in the completed category analysis.

**Business interpretation:** Storage is the strongest demand segment and should receive particular attention in forecasting, inventory availability, and operational planning.

### Demand pattern
The monthly demand trend showed a **seasonal pattern** rather than a flat trend.

**Business interpretation:** Time-dependent features are important for demand forecasting and inventory planning.

### Top revenue SKU
**SKU408** generated the highest total revenue in the completed SKU revenue analysis.

**Business interpretation:** SKU408 is a high-value product and is appropriate for close monitoring of demand and availability.

### Lowest-selling SKU
**SKU418** was the lowest-selling SKU in the dead-stock analysis.

**Business interpretation:** SKU418 is a candidate for further slow-moving/dead-stock review.

## 3. Promotion Analysis
Average units sold were:

- No promotion (`promo_flag = 0`): **20.014555**
- Promotion (`promo_flag = 1`): **19.979317**

The difference is approximately **0.035 units per record**, indicating no material lift in average unit sales from the promotion flag in this dataset.

**Business interpretation:** Promotions should not automatically be assumed to be a strong demand driver for this dataset. Their usefulness should be tested by product/category and event type before being treated as a major forecasting driver.

## 4. Key Business Insights
1. Storage is the strongest unit-demand category.
2. Demand is seasonal, so the forecasting process should preserve time structure.
3. SKU408 is a high-revenue SKU and should be monitored closely.
4. SKU418 is a slow-moving candidate for inventory review.
5. The observed promotion flag did not materially increase average sales.

## 5. Limitations
The EDA findings are descriptive and do not by themselves prove causality. In particular, the promotion result should not be interpreted as proof that promotions never work; it only describes the relationship observed in the supplied data.

## 6. Conclusion
The EDA supports a time-series forecasting approach and provides clear business areas for inventory attention, including high-value products, slow movers, and seasonal demand behavior.
