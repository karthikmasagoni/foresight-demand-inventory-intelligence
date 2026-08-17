import numpy as np
import pandas as pd


def calculate_inventory_metrics(decision_data):
    """Calculate demand and inventory risk metrics."""

    data = decision_data.copy()

    data["forecast_4_weeks"] = (
        data["forecast_week_1"]
        + data["forecast_week_2"]
        + data["forecast_week_3"]
        + data["forecast_week_4"]
    )

    data["avg_weekly_forecast"] = (
        data["forecast_4_weeks"] / 4
    )

    data["lead_time_weeks"] = (
        data["lead_time_days"] / 7
    )

    data["lead_time_demand"] = (
        data["avg_weekly_forecast"]
        * data["lead_time_weeks"]
    )

    data["available_inventory"] = (
        data["on_hand_units"]
        + data["on_order_units"]
    )

    data["stockout_gap"] = (
        data["lead_time_demand"]
        - data["available_inventory"]
    )

    data["stockout_risk"] = np.where(
        data["stockout_gap"] > 0,
        "HIGH",
        "LOW"
    )

    data["overstock_threshold"] = (
        data["forecast_4_weeks"] * 1.5
    )

    data["overstock_risk"] = np.where(
        data["on_hand_units"]
        > data["overstock_threshold"],
        "HIGH",
        "LOW"
    )

    return data


def calculate_volatility(
    weekly_sales,
    recent_weeks=8
):
    """Calculate demand volatility by SKU."""

    recent = (
        weekly_sales
        .sort_values(["sku_id", "date"])
        .groupby("sku_id")
        .tail(recent_weeks)
    )

    volatility = (
        recent
        .groupby("sku_id")["units_sold"]
        .agg(
            demand_mean="mean",
            demand_std="std"
        )
        .reset_index()
    )

    volatility["cv"] = (
        volatility["demand_std"]
        / volatility["demand_mean"]
        .replace(0, np.nan)
    )

    return volatility


def assign_actions(
    decision_data,
    volatility_threshold=None
):
    """Assign the client's four business actions."""

    data = decision_data.copy()

    if volatility_threshold is None:
        volatility_threshold = data["cv"].quantile(0.90)

    def get_action(row):

        if row["stockout_risk"] == "HIGH":
            return "REORDER NOW"

        if row["overstock_risk"] == "HIGH":
            return "MARKDOWN/CLEAR"

        if (
            pd.notna(row["cv"])
            and row["cv"] >= volatility_threshold
        ):
            return "WATCH/VOLATILE"

        return "HEALTHY"

    data["action"] = data.apply(
        get_action,
        axis=1
    )

    return data, volatility_threshold


def calculate_sales_at_risk(data):
    """Estimate sales value associated with stockout gap."""

    data = data.copy()

    data["sales_at_risk"] = (
        data["stockout_gap"]
        .clip(lower=0)
        * data["list_price"]
    )

    return data