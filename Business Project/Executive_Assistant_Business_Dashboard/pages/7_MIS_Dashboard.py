import streamlit as st
import pandas as pd
import plotly.express as px

from utils.data_loader import load_data
from utils.sidebar import create_sidebar

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="Executive MIS Dashboard",
    layout="wide"
)

create_sidebar()

st.title("Executive MIS Dashboard")
st.caption("Executive Assistant Business Intelligence Dashboard")

st.divider()

# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

data = load_data()

meeting_df = data["meetings"]
task_df = data["tasks"]
followup_df = data["followups"]
vendor_df = data["vendors"]
expense_df = data["expenses"]
calendar_df = data["calendar"]

expense_df["Expense_Date"] = pd.to_datetime(expense_df["Expense_Date"])
calendar_df["Date"] = pd.to_datetime(calendar_df["Date"])

# --------------------------------------------------
# KPI CALCULATIONS
# --------------------------------------------------

total_meetings = len(meeting_df)

total_tasks = len(task_df)

completed_tasks = (
    task_df["Status"]
    .astype(str)
    .str.lower()
    .eq("completed")
    .sum()
)

pending_followups = (
    followup_df["Status"]
    .astype(str)
    .str.lower()
    .eq("pending")
    .sum()
)

total_vendors = len(vendor_df)

total_expense = expense_df["Amount"].sum()

working_hours = calendar_df["Total_Working_Hours"].sum()

focus_hours = calendar_df["Focus_Hours"].sum()

productivity = round(
    (focus_hours / working_hours) * 100,
    2
)

# --------------------------------------------------
# KPI CARDS
# --------------------------------------------------

st.subheader("Executive KPIs")

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Meetings",
    total_meetings
)

c2.metric(
    "Tasks Completed",
    completed_tasks
)

c3.metric(
    "Pending Follow-ups",
    pending_followups
)

c4.metric(
    "Total Vendors",
    total_vendors
)

c5, c6, c7, c8 = st.columns(4)

c5.metric(
    "Total Expense",
    f"₹ {total_expense:,.0f}"
)

c6.metric(
    "Working Hours",
    round(working_hours,2)
)

c7.metric(
    "Focus Hours",
    round(focus_hours,2)
)

c8.metric(
    "Productivity",
    f"{productivity}%"
)

st.divider()

# --------------------------------------------------
# CHARTS
# --------------------------------------------------

left, right = st.columns(2)

with left:

    meeting_chart = (
        meeting_df
        .groupby("Status")
        .size()
        .reset_index(name="Meetings")
    )

    fig = px.pie(
        meeting_chart,
        names="Status",
        values="Meetings",
        title="Meeting Status"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with right:

    task_chart = (
        task_df
        .groupby("Status")
        .size()
        .reset_index(name="Tasks")
    )

    fig = px.bar(
        task_chart,
        x="Status",
        y="Tasks",
        color="Status",
        title="Task Status"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

st.divider()

# --------------------------------------------------
# EXPENSES & VENDORS
# --------------------------------------------------

left, right = st.columns(2)

with left:

    dept = (
        expense_df
        .groupby("Department")["Amount"]
        .sum()
        .reset_index()
    )

    fig = px.bar(
        dept,
        x="Department",
        y="Amount",
        color="Department",
        title="Department Expenses"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with right:

    vendor = (
        vendor_df
        .groupby("Category")
        .size()
        .reset_index(name="Vendors")
    )

    fig = px.pie(
        vendor,
        names="Category",
        values="Vendors",
        title="Vendor Categories"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

st.divider()

# --------------------------------------------------
# CALENDAR
# --------------------------------------------------

calendar_chart = calendar_df.copy()

fig = px.line(
    calendar_chart,
    x="Date",
    y="Total_Working_Hours",
    markers=True,
    title="Working Hours Trend"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.divider()

# --------------------------------------------------
# MONTHLY EXPENSE TREND
# --------------------------------------------------

monthly = (
    expense_df
    .groupby(expense_df["Expense_Date"].dt.to_period("M"))["Amount"]
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

# --------------------------------------------------
# EXECUTIVE SUMMARY TABLE
# --------------------------------------------------

summary = pd.DataFrame({

    "Metric":[

        "Meetings",

        "Tasks",

        "Completed Tasks",

        "Pending Follow-ups",

        "Vendors",

        "Total Expense",

        "Working Hours",

        "Productivity"

    ],

    "Value":[

        total_meetings,

        total_tasks,

        completed_tasks,

        pending_followups,

        total_vendors,

        f"₹ {total_expense:,.0f}",

        round(working_hours,2),

        f"{productivity}%"

    ]

})

st.subheader("Executive Summary")

st.dataframe(
    summary,
    use_container_width=True,
    hide_index=True
)

st.divider()

# --------------------------------------------------
# EXECUTIVE INSIGHTS
# --------------------------------------------------

highest_department = (
    expense_df
    .groupby("Department")["Amount"]
    .sum()
    .idxmax()
)

highest_vendor = (
    expense_df
    .groupby("Vendor")["Amount"]
    .sum()
    .idxmax()
)

st.success(f"""

EXECUTIVE INSIGHTS

• Total Meetings : {total_meetings}

• Completed Tasks : {completed_tasks}

• Pending Follow-ups : {pending_followups}

• Total Vendors : {total_vendors}

• Highest Spending Department : {highest_department}

• Highest Expense Vendor : {highest_vendor}

• Overall Productivity : {productivity}%

• Total Expense : ₹ {total_expense:,.0f}

""")