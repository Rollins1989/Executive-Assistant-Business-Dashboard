import streamlit as st
import pandas as pd
import plotly.express as px

from utils.data_loader import load_data
from utils.sidebar import create_sidebar

# ----------------------------------------------------
# PAGE CONFIG
# ----------------------------------------------------

st.set_page_config(
    page_title="Expense Dashboard",
    layout="wide"
)

create_sidebar()

st.title("Expense Dashboard")
st.caption("Executive Assistant Business Dashboard")

st.divider()

# ----------------------------------------------------
# LOAD DATA
# ----------------------------------------------------

data = load_data()

expense_df = data["expenses"]

expense_df["Expense_Date"] = pd.to_datetime(expense_df["Expense_Date"])

# ----------------------------------------------------
# FILTERS
# ----------------------------------------------------

st.subheader("Filters")

col1, col2, col3 = st.columns(3)

with col1:

    department = st.selectbox(
        "Department",
        ["All"] + sorted(expense_df["Department"].dropna().unique().tolist())
    )

with col2:

    category = st.selectbox(
        "Category",
        ["All"] + sorted(expense_df["Category"].dropna().unique().tolist())
    )

with col3:

    approval = st.selectbox(
        "Approval Status",
        ["All"] + sorted(expense_df["Approval_Status"].dropna().unique().tolist())
    )

# ----------------------------------------------------
# APPLY FILTERS
# ----------------------------------------------------

filtered = expense_df.copy()

if department != "All":
    filtered = filtered[
        filtered["Department"] == department
    ]

if category != "All":
    filtered = filtered[
        filtered["Category"] == category
    ]

if approval != "All":
    filtered = filtered[
        filtered["Approval_Status"] == approval
    ]

# ----------------------------------------------------
# KPI SECTION
# ----------------------------------------------------

st.subheader("Expense KPIs")

k1, k2, k3, k4 = st.columns(4)

total_expense = filtered["Amount"].sum()

average_expense = filtered["Amount"].mean()

highest_expense = filtered["Amount"].max()

transactions = len(filtered)

k1.metric(
    "Total Expense",
    f"₹ {total_expense:,.0f}"
)

k2.metric(
    "Average Expense",
    f"₹ {average_expense:,.0f}"
)

k3.metric(
    "Highest Expense",
    f"₹ {highest_expense:,.0f}"
)

k4.metric(
    "Transactions",
    transactions
)

st.divider()

# ----------------------------------------------------
# MONTHLY EXPENSE TREND
# ----------------------------------------------------

monthly = (
    filtered
    .groupby(filtered["Expense_Date"].dt.to_period("M"))["Amount"]
    .sum()
    .reset_index()
)

monthly["Expense_Date"] = monthly["Expense_Date"].astype(str)

fig = px.line(
    monthly,
    x="Expense_Date",
    y="Amount",
    markers=True,
    title="Monthly Expense Trend"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.divider()

# ----------------------------------------------------
# CHARTS
# ----------------------------------------------------

left, right = st.columns(2)

with left:

    dept = (
        filtered
        .groupby("Department")["Amount"]
        .sum()
        .reset_index()
    )

    fig = px.bar(
        dept,
        x="Department",
        y="Amount",
        color="Department",
        title="Expense by Department"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with right:

    cat = (
        filtered
        .groupby("Category")["Amount"]
        .sum()
        .reset_index()
    )

    fig = px.pie(
        cat,
        names="Category",
        values="Amount",
        title="Expense by Category"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

st.divider()

# ----------------------------------------------------
# PAYMENT MODE
# ----------------------------------------------------

left, right = st.columns(2)

with left:

    payment = (
        filtered
        .groupby("Payment_Mode")
        .size()
        .reset_index(name="Transactions")
    )

    fig = px.bar(
        payment,
        x="Payment_Mode",
        y="Transactions",
        color="Payment_Mode",
        title="Payment Mode Distribution"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with right:

    approval_df = (
        filtered
        .groupby("Approval_Status")
        .size()
        .reset_index(name="Count")
    )

    fig = px.pie(
        approval_df,
        names="Approval_Status",
        values="Count",
        title="Approval Status"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

st.divider()

# ----------------------------------------------------
# TOP VENDORS
# ----------------------------------------------------

vendor = (
    filtered
    .groupby("Vendor")["Amount"]
    .sum()
    .reset_index()
    .sort_values("Amount", ascending=False)
)

fig = px.bar(
    vendor,
    x="Vendor",
    y="Amount",
    color="Amount",
    title="Vendor-wise Expenses"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.divider()

# ----------------------------------------------------
# TABLE
# ----------------------------------------------------

st.subheader("Expense Records")

st.dataframe(
    filtered,
    use_container_width=True,
    hide_index=True
)

st.divider()

# ----------------------------------------------------
# EXECUTIVE INSIGHTS
# ----------------------------------------------------

st.subheader("Executive Insights")

highest_department = (
    filtered
    .groupby("Department")["Amount"]
    .sum()
    .idxmax()
)

highest_vendor = (
    filtered
    .groupby("Vendor")["Amount"]
    .sum()
    .idxmax()
)

highest_amount = filtered["Amount"].max()

st.success(f"""
Highest Spending Department : {highest_department}

Highest Expense Vendor : {highest_vendor}

Largest Single Expense : ₹ {highest_amount:,.0f}

Total Transactions : {transactions}
""")