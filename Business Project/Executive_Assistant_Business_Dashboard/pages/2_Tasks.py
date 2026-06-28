import streamlit as st
import pandas as pd
import plotly.express as px

from utils.data_loader import load_data
from utils.sidebar import create_sidebar
from utils.header import dashboard_header

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------

st.set_page_config(
    page_title="Task Dashboard",
    layout="wide"
)

create_sidebar()

dashboard_header("Task Dashboard")

# ---------------------------------------------------
# LOAD DATA
# ---------------------------------------------------

data = load_data()

task_df = data["tasks"]

# ---------------------------------------------------
# FILTERS
# ---------------------------------------------------

st.subheader("Task Filters")

col1, col2 = st.columns(2)

with col1:

    status = st.selectbox(
        "Task Status",
        ["All"] + sorted(task_df["Status"].dropna().unique().tolist())
    )

with col2:

    priority = st.selectbox(
        "Priority",
        ["All"] + sorted(task_df["Priority"].dropna().unique().tolist())
    )

# ---------------------------------------------------
# APPLY FILTERS
# ---------------------------------------------------

filtered = task_df.copy()

if status != "All":
    filtered = filtered[
        filtered["Status"] == status
    ]

if priority != "All":
    filtered = filtered[
        filtered["Priority"] == priority
    ]

# ---------------------------------------------------
# KPI SECTION
# ---------------------------------------------------

st.subheader("Task KPIs")

k1, k2, k3, k4 = st.columns(4)

completed = (
    filtered["Status"] == "Completed"
).sum()

pending = (
    filtered["Status"] == "Pending"
).sum()

in_progress = (
    filtered["Status"] == "In Progress"
).sum()

overdue = (
    filtered["Status"] == "Overdue"
).sum()

k1.metric(
    "Total Tasks",
    len(filtered)
)

k2.metric(
    "Completed",
    completed
)

k3.metric(
    "Pending",
    pending
)

k4.metric(
    "Overdue",
    overdue
)

st.divider()

# ---------------------------------------------------
# CHARTS
# ---------------------------------------------------

left, right = st.columns(2)

with left:

    fig = px.pie(
        filtered,
        names="Status",
        title="Task Status Distribution"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with right:

    priority_df = (
        filtered
        .groupby("Priority")
        .size()
        .reset_index(name="Tasks")
    )

    fig = px.bar(
        priority_df,
        x="Priority",
        y="Tasks",
        color="Priority",
        title="Priority Distribution"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

st.divider()

owner_df = (
    filtered
    .groupby("Owner")
    .size()
    .reset_index(name="Tasks")
)

fig = px.bar(
    owner_df,
    x="Owner",
    y="Tasks",
    title="Task Allocation by Owner"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ---------------------------------------------------
# TASK TABLE
# ---------------------------------------------------

st.subheader("Task Records")

st.dataframe(
    filtered,
    use_container_width=True,
    hide_index=True
)

# ---------------------------------------------------
# EXECUTIVE INSIGHTS
# ---------------------------------------------------

st.divider()

st.subheader("Executive Insights")

completion_rate = round(
    (completed / len(filtered)) * 100,
    2
) if len(filtered) > 0 else 0

highest_priority = (
    filtered["Priority"]
    .mode()[0]
    if not filtered.empty
    else "N/A"
)

st.success(
    f"""
Completion Rate : {completion_rate}%

Most Common Priority : {highest_priority}

Pending Tasks : {pending}

Overdue Tasks : {overdue}
"""
)