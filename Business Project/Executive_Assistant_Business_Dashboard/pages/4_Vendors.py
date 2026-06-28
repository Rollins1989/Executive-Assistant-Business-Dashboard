import streamlit as st
import pandas as pd
import plotly.express as px

from utils.data_loader import load_data
from utils.sidebar import create_sidebar

# ----------------------------------------------------
# PAGE CONFIG
# ----------------------------------------------------

st.set_page_config(
    page_title="Vendor Dashboard",
    layout="wide"
)

create_sidebar()

st.title("Vendor Dashboard")
st.caption("Executive Assistant Business Dashboard")

st.divider()

# ----------------------------------------------------
# LOAD DATA
# ----------------------------------------------------

data = load_data()

vendor_df = data["vendors"]

# ----------------------------------------------------
# FILTERS
# ----------------------------------------------------

st.subheader("Filters")

col1, col2 = st.columns(2)

with col1:

    category = st.selectbox(
        "Category",
        ["All"] + sorted(vendor_df["Category"].dropna().unique().tolist())
    )

with col2:

    payment = st.selectbox(
        "Payment Status",
        ["All"] + sorted(vendor_df["Payment_Status"].dropna().unique().tolist())
    )

# ----------------------------------------------------
# APPLY FILTERS
# ----------------------------------------------------

filtered = vendor_df.copy()

if category != "All":
    filtered = filtered[
        filtered["Category"] == category
    ]

if payment != "All":
    filtered = filtered[
        filtered["Payment_Status"] == payment
    ]

# ----------------------------------------------------
# KPI SECTION
# ----------------------------------------------------

st.subheader("Vendor KPIs")

k1, k2, k3, k4 = st.columns(4)

total_vendors = len(filtered)

active_contract = (
    filtered["Contract_Value"]
    .sum()
)

paid = (
    filtered["Payment_Status"] == "Paid"
).sum()

pending = (
    filtered["Payment_Status"] == "Pending"
).sum()

k1.metric(
    "Total Vendors",
    total_vendors
)

k2.metric(
    "Contract Value",
    f"₹ {active_contract:,.0f}"
)

k3.metric(
    "Paid",
    paid
)

k4.metric(
    "Pending",
    pending
)

st.divider()

# ----------------------------------------------------
# CHARTS
# ----------------------------------------------------

left, right = st.columns(2)

with left:

    fig = px.pie(
        filtered,
        names="Payment_Status",
        title="Payment Status Distribution"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with right:

    category_df = (
        filtered
        .groupby("Category")
        .size()
        .reset_index(name="Vendors")
    )

    fig = px.bar(
        category_df,
        x="Category",
        y="Vendors",
        color="Category",
        title="Vendor Category Distribution"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

st.divider()

# ----------------------------------------------------
# CONTRACT VALUE
# ----------------------------------------------------

contract_df = (
    filtered
    .sort_values(
        "Contract_Value",
        ascending=False
    )
)

fig = px.bar(
    contract_df,
    x="Vendor_Name",
    y="Contract_Value",
    color="Category",
    title="Contract Value by Vendor"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.divider()

# ----------------------------------------------------
# DATA TABLE
# ----------------------------------------------------

st.subheader("Vendor Records")

st.dataframe(
    filtered,
    use_container_width=True,
    hide_index=True
)

# ----------------------------------------------------
# EXECUTIVE INSIGHTS
# ----------------------------------------------------

st.divider()

st.subheader("Executive Insights")

highest_vendor = (
    filtered
    .sort_values(
        "Contract_Value",
        ascending=False
    )
    .iloc[0]["Vendor_Name"]
)

highest_value = (
    filtered["Contract_Value"]
    .max()
)

st.success(
    f"""
Highest Contract Vendor : {highest_vendor}

Highest Contract Value : ₹ {highest_value:,.0f}

Total Vendors : {total_vendors}

Pending Payments : {pending}
"""
)