import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor


FEATURES = [
    "lag_1",
    "lag_2",
    "lag_4",
    "rolling_4",
]


def create_weekly_demand(sales):
    """Convert daily sales into weekly SKU-level demand."""
    return (
        sales
        .groupby(
            ["sku_id", pd.Grouper(key="date", freq="W")]
        )["units_sold"]
        .sum()
        .reset_index()
        .sort_values(["sku_id", "date"])
    )


def create_forecasting_features(weekly_sales):
    """Create lag, rolling, and seasonal-naive features."""
    weekly = weekly_sales.copy()

    weekly["lag_1"] = (
        weekly.groupby("sku_id")["units_sold"]
        .shift(1)
    )

    weekly["lag_2"] = (
        weekly.groupby("sku_id")["units_sold"]
        .shift(2)
    )

    weekly["lag_4"] = (
        weekly.groupby("sku_id")["units_sold"]
        .shift(4)
    )

    weekly["rolling_4"] = (
        weekly.groupby("sku_id")["units_sold"]
        .transform(
            lambda x: x.shift(1).rolling(4).mean()
        )
    )

    weekly["seasonal_naive"] = (
        weekly.groupby("sku_id")["units_sold"]
        .shift(52)
    )

    return weekly


def train_forecast_model(model_data):
    """Train the Random Forest forecasting model."""
    model = RandomForestRegressor(
        n_estimators=200,
        random_state=42,
        n_jobs=-1
    )

    model.fit(
        model_data[FEATURES],
        model_data["units_sold"]
    )

    return model


def generate_next_4_week_forecast(model, weekly_sales):
    """Generate recursive 4-week forecasts for every SKU."""

    latest_history = (
        weekly_sales
        .sort_values(["sku_id", "date"])
        .groupby("sku_id")
        .tail(4)
    )

    history = (
        latest_history
        .groupby("sku_id")["units_sold"]
        .apply(list)
        .to_dict()
    )

    forecast_table = pd.DataFrame({
        "sku_id": sorted(history.keys())
    })

    for week in range(1, 5):

        predictions = []

        for sku in forecast_table["sku_id"]:

            values = history[sku]

            model_input = pd.DataFrame([{
                "lag_1": values[-1],
                "lag_2": values[-2],
                "lag_4": values[-4],
                "rolling_4": np.mean(values[-4:])
            }])

            prediction = model.predict(model_input)[0]

            # Demand should not be negative
            prediction = max(0, prediction)

            predictions.append(prediction)

        forecast_table[
            f"forecast_week_{week}"
        ] = predictions

        for i, sku in enumerate(
            forecast_table["sku_id"]
        ):
            history[sku].append(predictions[i])
            history[sku] = history[sku][-4:]

    return forecast_table


def calculate_wape(actual, predicted):
    """Calculate WAPE."""
    denominator = np.abs(actual).sum()

    if denominator == 0:
        return np.nan

    return (
        np.abs(actual - predicted).sum()
        / denominator
    )


def calculate_bias(actual, predicted):
    """Calculate forecast bias."""
    denominator = np.abs(actual).sum()

    if denominator == 0:
        return np.nan

    return (
        (actual - predicted).sum()
        / denominator
    )