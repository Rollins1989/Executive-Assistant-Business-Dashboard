import streamlit as st
import pandas as pd
import plotly.express as px
from utils.sidebar import create_sidebar

create_sidebar()
from utils.data_loader import load_data

# --------------------------------------
# PAGE CONFIG
# --------------------------------------

st.set_page_config(
    page_title="Meetings",
    layout="wide"
)

# --------------------------------------
# LOAD DATA
# --------------------------------------

data = load_data()

meeting_df = data["meetings"]

# --------------------------------------
# PAGE TITLE
# --------------------------------------

st.title("Meeting Analytics")

st.caption("Executive Assistant Dashboard")

st.divider()

# --------------------------------------
# FILTERS
# --------------------------------------

col1, col2 = st.columns(2)

status = col1.selectbox(
    "Meeting Status",
    ["All"] + sorted(meeting_df["Status"].dropna().unique())
)

department = col2.selectbox(
    "Department",
    ["All"] + sorted(meeting_df["Department"].dropna().unique())
)

filtered = meeting_df.copy()

if status != "All":
    filtered = filtered[
        filtered["Status"] == status
    ]

if department != "All":
    filtered = filtered[
        filtered["Department"] == department
    ]

st.divider()

# --------------------------------------
# KPIs
# --------------------------------------

k1, k2, k3 = st.columns(3)

k1.metric(
    "Meetings",
    len(filtered)
)

k2.metric(
    "Meeting Hours",
    round(filtered["Duration_Minutes"].sum()/60,2)
)

k3.metric(
    "Departments",
    filtered["Department"].nunique()
)

st.divider()

# --------------------------------------
# CHARTS
# --------------------------------------

left, right = st.columns(2)

with left:

    fig = px.pie(
        filtered,
        names="Status",
        title="Meeting Status"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with right:

    dept = (
        filtered
        .groupby("Department")
        .size()
        .reset_index(name="Meetings")
    )

    fig = px.bar(
        dept,
        x="Department",
        y="Meetings",
        title="Meetings by Department"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

st.divider()

st.subheader("Meeting Records")

st.dataframe(
    filtered,
    use_container_width=True
)
