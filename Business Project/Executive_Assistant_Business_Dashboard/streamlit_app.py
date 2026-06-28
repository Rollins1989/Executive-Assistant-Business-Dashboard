import streamlit as st
import pandas as pd
import plotly.express as px
import os
from utils.charts import *
from datetime import datetime
from utils.metrics import kpi_card
from utils.data_loader import load_data
from utils.theme import load_css
from utils.sidebar import create_sidebar
# ----------------------------------------------------
# PAGE CONFIGURATION
# ----------------------------------------------------

st.set_page_config(
    page_title="Executive Assistant Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)
st.sidebar.title("Navigation")

st.sidebar.markdown("---")

st.sidebar.info(
    """
Executive Assistant Dashboard

Version 1.0

Business Intelligence Suite
"""
)

# ----------------------------------------------------
# LOAD DATA
# ----------------------------------------------------

data = load_data()

meeting_df = data["meetings"]
task_df = data["tasks"]
followup_df = data["followups"]
vendor_df = data["vendors"]
expense_df = data["expenses"]
calendar_df = data["calendar"]

# ----------------------------------------------------
# DASHBOARD FILTERS
# ----------------------------------------------------

st.subheader("Dashboard Filters")

filter1, filter2 = st.columns(2)

department = "All"
meeting_status = "All"

with filter1:
    department = st.selectbox(
        "Department",
        ["All"] + sorted(expense_df["Department"].dropna().unique().tolist())
    )

with filter2:
    meeting_status = st.selectbox(
        "Meeting Status",
        ["All"] + sorted(meeting_df["Status"].dropna().unique().tolist())
    )

# -----------------------------
# Apply Filters
# -----------------------------

filtered_expense_df = expense_df.copy()
filtered_meeting_df = meeting_df.copy()

if department != "All":
    filtered_expense_df = filtered_expense_df[
        filtered_expense_df["Department"] == department
    ]

if meeting_status != "All":
    filtered_meeting_df = filtered_meeting_df[
        filtered_meeting_df["Status"] == meeting_status
    ]
# ----------------------------------------------------
# HEADER
# ----------------------------------------------------

st.title("Executive Assistant Business Dashboard")

st.caption(
    f"Last Updated : {datetime.now().strftime('%d %B %Y %I:%M %p')}"
)

st.divider()

# ----------------------------------------------------
# KPI CALCULATIONS
# ----------------------------------------------------

total_meetings = len(meeting_df)

total_tasks = len(task_df)

total_followups = len(followup_df)

total_vendors = len(vendor_df)

total_expense = expense_df["Amount"].sum()

working_hours = calendar_df["Total_Working_Hours"].sum()

focus_hours = calendar_df["Focus_Hours"].sum()

productivity = round(
    (focus_hours / working_hours) * 100,
    2
)

utilization = round(
    (working_hours / (365 * 8)) * 100,
    2
)

# ----------------------------------------------------
# KPI ROW 1
# ----------------------------------------------------

col1, col2, col3, col4 = st.columns(4)

with col1:
    kpi_card("Meetings", total_meetings, "#2563EB")

with col2:
    kpi_card("Tasks", total_tasks, "#16A34A")

with col3:
    kpi_card("Follow-ups", total_followups, "#F59E0B")

with col4:
    kpi_card("Vendors", total_vendors, "#9333EA")

# ----------------------------------------------------
# KPI ROW 2
# ----------------------------------------------------

col5, col6, col7, col8 = st.columns(4)

with col5:
    kpi_card(
        "Expenses",
        f"₹ {total_expense:,.0f}",
        "#DC2626"
    )

with col6:
    kpi_card(
        "Working Hours",
        working_hours,
        "#0891B2"
    )

with col7:
    kpi_card(
        "Productivity",
        f"{productivity}%",
        "#059669"
    )

with col8:
    kpi_card(
        "Utilization",
        f"{utilization}%",
        "#7C3AED"
    )

st.subheader("Dashboard Summary")

summary1, summary2, summary3 = st.columns(3)

with summary1:
    st.metric(
        "Average Expense",
        f"₹ {expense_df['Amount'].mean():,.0f}"
    )

with summary2:
    st.metric(
        "Highest Expense",
        f"₹ {expense_df['Amount'].max():,.0f}"
    )

with summary3:
    st.metric(
        "Completed Tasks",
        (task_df["Status"] == "Completed").sum()
    )

st.divider()

st.subheader("Business Overview")

left, right = st.columns([2,1])

with left:

    st.write(
        """
This dashboard consolidates operational information from meetings,
tasks, follow-ups, vendors, expenses and calendar activities.

Use the navigation menu on the left to analyze each business area
individually or open the Executive MIS Dashboard for a complete
organizational overview.
"""
    )

with right:

    st.info(
        """
Dashboard Status

Operational

Data Source

Excel Database

Refresh

Manual
"""
    )

st.divider()

st.subheader("Business Analytics")

left, right = st.columns(2)

with left:

    st.plotly_chart(

       meeting_status_chart(filtered_meeting_df),

        use_container_width=True

    )

with right:

    st.plotly_chart(

        task_status_chart(task_df),

        use_container_width=True

    )

st.divider()

st.plotly_chart(

    expense_department_chart(filtered_expense_df),

    use_container_width=True

)

activity = [

"Meeting Tracker Updated",

"Expense Report Generated",

"Vendor Summary Exported",

"Task Dashboard Refreshed",

"Calendar Analytics Updated"

]

for item in activity:

    st.write("•", item)

def load_css():

    css_file = os.path.join(
        "assets",
        "style.css"
    )

    with open(css_file) as f:

        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True
        )

load_css()

st.divider()

st.subheader("Executive Insights")

highest_dept = (
    expense_df.groupby("Department")["Amount"]
    .sum()
    .idxmax()
)

highest_amount = (
    expense_df.groupby("Department")["Amount"]
    .sum()
    .max()
)

completed_tasks = (
    task_df["Status"] == "Completed"
).sum()

pending_tasks = (
    task_df["Status"] == "Pending"
).sum()

st.success(
    f"""
Highest spending department: {highest_dept}

Total spend: ₹ {highest_amount:,.0f}

Completed Tasks: {completed_tasks}

Pending Tasks: {pending_tasks}

Productivity: {productivity}%
"""
)

st.divider()

st.subheader("Download Reports")

with open(
    "reports/Executive_Report.pdf",
    "rb"
) as file:

    st.download_button(
        label="Download Executive PDF Report",
        data=file,
        file_name="Executive_Report.pdf",
        mime="application/pdf"
    )