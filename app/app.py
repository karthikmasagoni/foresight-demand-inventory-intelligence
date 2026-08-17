import streamlit as st
import pandas as pd
import sys
from pathlib import Path

st.set_page_config(
    page_title="FORESIGHT",
    page_icon="📦",
    layout="wide"
)

sys.path.append(
    str(Path(__file__).resolve().parent.parent)
)

from src.auth import (
    init_db,
    register_user,
    verify_user
)

init_db()




if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if "username" not in st.session_state:
    st.session_state.username = None


if not st.session_state.authenticated:

    st.title("FORESIGHT")
    st.subheader("Demand & Inventory Intelligence")

    tab1, tab2 = st.tabs(
        ["Login", "Register"]
    )

    
    with tab1:

        st.subheader("Welcome Back")

        username = st.text_input(
            "Username",
            key="login_username"
        )

        password = st.text_input(
            "Password",
            type="password",
            key="login_password"
        )

        if st.button(
            "Login",
            use_container_width=True
        ):

            if verify_user(
                username,
                password
            ):

                st.session_state.authenticated = True
                st.session_state.username = username

                st.success(
                    "Login successful."
                )

                st.rerun()

            else:

                st.error(
                    "Invalid username or password."
                )

    
    with tab2:

        st.subheader(
            "Create Your FORESIGHT Account"
        )

        col1, col2 = st.columns(2)

        with col1:

            full_name = st.text_input(
                "Full Name *",
                placeholder="Enter your full name",
                key="register_full_name"
            )

            email = st.text_input(
                "Email Address *",
                placeholder="name@example.com",
                key="register_email"
            )

            username = st.text_input(
                "Username *",
                placeholder="Choose a username",
                key="register_username"
            )

        with col2:

            gender = st.selectbox(
                "Gender",
                [
                    "Prefer not to say",
                    "Male",
                    "Female",
                    "Other"
                ],
                key="register_gender"
            )

            password = st.text_input(
                "Password *",
                type="password",
                placeholder="Create a strong password",
                key="register_password"
            )

            confirm_password = st.text_input(
                "Confirm Password *",
                type="password",
                placeholder="Re-enter your password",
                key="register_confirm_password"
            )

        st.caption("* Required fields")

        if st.button(
            "Create Account",
            use_container_width=True
        ):

            if password != confirm_password:

                st.error(
                    "Passwords do not match."
                )

            else:

                success, message = register_user(
                    full_name,
                    email,
                    gender,
                    username,
                    password
                )

                if success:

                    st.success(message)

                    st.info(
                        "Your account has been created. "
                        "Please switch to the Login tab."
                    )

                else:

                    st.error(message)

    st.stop()





@st.cache_data
def load_decision_data():

    return pd.read_csv(
        "data/foresight_decisions.csv"
    )


@st.cache_data
def load_forecast_actual():

    df = pd.read_csv(
        "data/forecast_actual.csv"
    )

    df["date"] = pd.to_datetime(df["date"])

    return df



data = load_decision_data()
forecast_actual = load_forecast_actual()

st.title("FORESIGHT")
st.subheader("Demand & Inventory Intelligence")

total_skus = data["sku_id"].nunique()

reorder_count = (
    data["action"] == "REORDER NOW"
).sum()

markdown_count = (
    data["action"] == "MARKDOWN/CLEAR"
).sum()

watch_count = (
    data["action"] == "WATCH/VOLATILE"
).sum()

healthy_count = (
    data["action"] == "HEALTHY"
).sum()


sales_at_risk = (
    data["sales_at_risk"].clip(lower=0).sum()
    if "sales_at_risk" in data.columns
    else 0
)

inventory_value = (
    data["on_hand_units"] * data["unit_cost"]
).sum()

high_stockout = (
    data["stockout_risk"] == "HIGH"
).sum()

high_overstock = (
    data["overstock_risk"] == "HIGH"
).sum()


col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("Total SKUs", total_skus)
col2.metric("Reorder Now", reorder_count)
col3.metric("Markdown / Clear", markdown_count)
col4.metric("Watch", watch_count)
col5.metric("Healthy", healthy_count)

st.divider()

st.subheader("Business Impact")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Sales Value at Risk",
    f"₹{sales_at_risk:,.0f}"
)

col2.metric(
    "Inventory Value",
    f"₹{inventory_value:,.0f}"
)

col3.metric(
    "High Stockout Risk",
    high_stockout
)

col4.metric(
    "High Overstock Risk",
    high_overstock
)

st.sidebar.header("Filters")

categories = sorted(
    data["category"]
    .dropna()
    .unique()
    .tolist()
)

selected_category = st.sidebar.selectbox(
    "Category",
    ["All"] + categories
)

filtered_data = data.copy()

if selected_category != "All":
    filtered_data = filtered_data[
        filtered_data["category"] == selected_category
    ]


sku_options = sorted(
    filtered_data["sku_id"]
    .dropna()
    .unique()
    .tolist()
)

selected_sku = st.selectbox(
    "Select SKU",
    sku_options
)

sku_data = filtered_data[
    filtered_data["sku_id"] == selected_sku
].iloc[0]


st.subheader(
    f"SKU Details: {selected_sku}"
)

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Current Stock",
    int(sku_data["on_hand_units"])
)

col2.metric(
    "On Order",
    int(sku_data["on_order_units"])
)

col3.metric(
    "4-Week Forecast",
    round(
        sku_data["forecast_4_weeks"],
        0
    )
)

col4.metric(
    "Decision",
    sku_data["action"]
)

st.subheader("Forecast vs Actual")

sku_history = forecast_actual[
    forecast_actual["sku_id"] == selected_sku
].sort_values("date")

if len(sku_history) > 0:

    chart_data = sku_history.set_index("date")[
        ["actual", "forecast"]
    ]

    st.line_chart(chart_data)

else:

    st.info(
        "No historical forecast/actual records "
        "are available for this SKU."
    )


st.subheader("Risk Assessment")

risk_df = pd.DataFrame({
    "Metric": [
        "Lead Time (days)",
        "Lead-Time Demand",
        "Available Inventory",
        "Stockout Risk",
        "Overstock Risk",
        "Volatility (CV)"
    ],
    "Value": [
        sku_data["lead_time_days"],
        round(
            sku_data["lead_time_demand"],
            1
        ),
        round(
            sku_data["available_inventory"],
            1
        ),
        sku_data["stockout_risk"],
        sku_data["overstock_risk"],
        round(
            sku_data["cv"],
            2
        )
    ]
})

st.dataframe(
    risk_df,
    use_container_width=True
)


st.divider()

st.subheader("Top Reorder Priorities")

reorder_list = (
    filtered_data[
        filtered_data["action"] == "REORDER NOW"
    ]
    .sort_values(
        "stockout_gap",
        ascending=False
    )
)

st.dataframe(
    reorder_list[
        [
            "sku_id",
            "category",
            "on_hand_units",
            "on_order_units",
            "lead_time_days",
            "lead_time_demand",
            "stockout_gap"
        ]
    ].head(20),
    use_container_width=True
)

st.subheader(
    "Top Markdown / Clear Priorities"
)

markdown_list = (
    filtered_data[
        filtered_data["action"] == "MARKDOWN/CLEAR"
    ]
    .sort_values(
        "on_hand_units",
        ascending=False
    )
)

st.dataframe(
    markdown_list[
        [
            "sku_id",
            "category",
            "on_hand_units",
            "forecast_4_weeks",
            "overstock_threshold"
        ]
    ].head(20),
    use_container_width=True
)