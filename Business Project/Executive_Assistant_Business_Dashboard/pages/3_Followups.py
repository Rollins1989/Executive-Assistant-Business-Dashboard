import streamlit as st
import pandas as pd
import plotly.express as px

from utils.data_loader import load_data
from utils.sidebar import create_sidebar

# -------------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------------

st.set_page_config(
    page_title="Follow-up Dashboard",
    layout="wide"
)

create_sidebar()

st.title("Follow-up Dashboard")
st.caption("Executive Assistant Business Dashboard")

st.divider()

# -------------------------------------------------------
# LOAD DATA
# -------------------------------------------------------

data = load_data()

followup_df = data["followups"]

# -------------------------------------------------------
# FILTERS
# -------------------------------------------------------

st.subheader("Filters")

col1, col2 = st.columns(2)

with col1:

    status = st.selectbox(
        "Status",
        ["All"] + sorted(
            followup_df["Status"].dropna().unique().tolist()
        )
    )

with col2:

    priority = st.selectbox(
        "Priority",
        ["All"] + sorted(
            followup_df["Priority"].dropna().unique().tolist()
        )
    )

# -------------------------------------------------------
# APPLY FILTERS
# -------------------------------------------------------

filtered = followup_df.copy()

if status != "All":
    filtered = filtered[
        filtered["Status"] == status
    ]

if priority != "All":
    filtered = filtered[
        filtered["Priority"] == priority
    ]

# -------------------------------------------------------
# KPIs
# -------------------------------------------------------

st.subheader("Follow-up KPIs")

k1, k2, k3, k4 = st.columns(4)

total = len(filtered)

completed = (
    filtered["Status"] == "Completed"
).sum()

pending = (
    filtered["Status"] == "Pending"
).sum()

overdue = (
    filtered["Status"] == "Overdue"
).sum()

k1.metric(
    "Total Follow-ups",
    total
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

# -------------------------------------------------------
# CHART 1
# -------------------------------------------------------

left, right = st.columns(2)

with left:

    fig = px.pie(
        filtered,
        names="Status",
        title="Follow-up Status"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# -------------------------------------------------------
# CHART 2
# -------------------------------------------------------

with right:

    priority_df = (
        filtered
        .groupby("Priority")
        .size()
        .reset_index(name="Count")
    )

    fig = px.bar(
        priority_df,
        x="Priority",
        y="Count",
        color="Priority",
        title="Priority Distribution"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

st.divider()

# -------------------------------------------------------
# OWNER ANALYSIS
# -------------------------------------------------------
person_df = (
    filtered
    .groupby("Person_Name")
    .size()
    .reset_index(name="Follow-ups")
)

fig = px.bar(
    person_df,
    x="Person_Name",
    y="Follow-ups",
    color="Follow-ups",
    title="Follow-ups by Person"
)

st.plotly_chart(
    fig,
    use_container_width=True
)
department_df = (
    filtered
    .groupby("Department")
    .size()
    .reset_index(name="Follow-ups")
)

fig = px.bar(
    department_df,
    x="Department",
    y="Follow-ups",
    color="Department",
    title="Department-wise Follow-ups"
)

st.plotly_chart(
    fig,
    use_container_width=True
)
# -------------------------------------------------------
# DATA TABLE
# -------------------------------------------------------

st.subheader("Follow-up Records")

st.dataframe(
    filtered,
    use_container_width=True,
    hide_index=True
)

# -------------------------------------------------------
# EXECUTIVE INSIGHTS
# -------------------------------------------------------

st.divider()

st.subheader("Executive Insights")

completion_rate = round(
    (completed / total) * 100,
    2
) if total > 0 else 0

most_common_priority = (
    filtered["Priority"].mode()[0]
    if not filtered.empty
    else "N/A"
)

st.success(
    f"""
Completion Rate : {completion_rate}%

Pending Follow-ups : {pending}

Overdue Follow-ups : {overdue}

Most Common Priority : {most_common_priority}
"""
)