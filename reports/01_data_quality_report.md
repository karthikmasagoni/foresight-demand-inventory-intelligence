# FORESIGHT — Data Quality Report

## 1. Purpose
This report documents the inspection, validation, integration, and known limitations of the four supplied datasets used for the FORESIGHT demand and inventory intelligence project.

## 2. Source Datasets
- `sales_daily.csv`
- `sku_master.xlsx`
- `calendar.xlsx`
- `inventory_snapshots.xlsx`

## 3. Data Quality Checks Performed

### Sales data
- Revenue was validated against `units_sold × unit_price`.
- Revenue mismatches: 0.
- Negative units sold: 0.
- Negative revenue: 0.
- Negative unit price: 0.
- Zero units sold: 0.
- Zero revenue: 0.
- Zero unit price: 0.
- `promo_flag` contained the expected binary values: 0 and 1.

### Key integrity
- Sales SKUs were checked against the SKU master.
- Inventory SKUs were checked against the SKU master.
- Duplicate SKU/date combinations were checked in sales and inventory.
- Sales-to-product merging preserved the original sales row count.
- Calendar merging used a left join to avoid dropping historical sales.

### Date coverage
The calendar extract covers 2025, while sales history extends earlier. Therefore, historical sales from 2023–2024 do not have corresponding calendar records in the supplied calendar file.

The inventory extract covers 2025. Consequently, older sales records do not have inventory snapshots.

These are data-availability limitations rather than reasons to delete the historical sales.

## 4. Missing-Value Interpretation
Some calendar fields such as `festival` and `promo_event` contain missing values. These were treated as "no recorded event" rather than automatically deleting rows.

Inventory fields are missing for historical periods where no inventory snapshot was supplied. These missing values were not interpreted as zero inventory.

## 5. Integration Approach
The principal keys used were:
- `sku_id` for product relationships
- `date` for calendar relationships
- `date + sku_id` for inventory relationships

The analytical workflow retained all sales records while attaching calendar and inventory information where available.

## 6. Cleaning Decisions
No artificial sales-value corrections were required because the core numerical validation checks passed.

Temporary diagnostic columns created during validation were removed after use.

## 7. Known Limitations
1. Calendar coverage is limited to 2025.
2. Inventory snapshots are limited to 2025.
3. Historical sales therefore have incomplete calendar/inventory context.
4. Prototype inventory thresholds should be reviewed with business stakeholders before production use.
5. Forecast uncertainty increases with recursive forecast horizon.

## 8. Conclusion
The supplied data was sufficiently consistent for forecasting and inventory-risk prototyping. The major limitations are coverage-related rather than basic data-integrity failures.
