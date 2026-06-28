import streamlit as st
import pandas as pd
import plotly.express as px

from utils.data_loader import load_data
from utils.sidebar import create_sidebar

# ----------------------------------------------------
# PAGE CONFIG
# ----------------------------------------------------

st.set_page_config(
    page_title="Calendar Analytics",
    layout="wide"
)

create_sidebar()

st.title("Calendar Analytics Dashboard")
st.caption("Executive Assistant Business Dashboard")

st.divider()

# ----------------------------------------------------
# LOAD DATA
# ----------------------------------------------------

data = load_data()

calendar_df = data["calendar"]

calendar_df["Date"] = pd.to_datetime(calendar_df["Date"])

# ----------------------------------------------------
# FILTERS
# ----------------------------------------------------

st.subheader("Filters")

col1, col2 = st.columns(2)

with col1:

    day = st.selectbox(
        "Day",
        ["All"] + sorted(calendar_df["Day"].dropna().unique().tolist())
    )

with col2:

    wfh = st.selectbox(
        "WFH",
        ["All"] + sorted(calendar_df["WFH"].astype(str).unique().tolist())
    )

# ----------------------------------------------------
# APPLY FILTERS
# ----------------------------------------------------

filtered = calendar_df.copy()

if day != "All":
    filtered = filtered[
        filtered["Day"] == day
    ]

if wfh != "All":
    filtered = filtered[
        filtered["WFH"].astype(str) == wfh
    ]

# ----------------------------------------------------
# KPI SECTION
# ----------------------------------------------------

st.subheader("Calendar KPIs")

k1, k2, k3, k4 = st.columns(4)

meeting_hours = filtered["Meeting_Hours"].sum()

focus_hours = filtered["Focus_Hours"].sum()

travel_hours = filtered["Travel_Hours"].sum()

working_hours = filtered["Total_Working_Hours"].sum()

k1.metric(
    "Meeting Hours",
    round(meeting_hours,2)
)

k2.metric(
    "Focus Hours",
    round(focus_hours,2)
)

k3.metric(
    "Travel Hours",
    round(travel_hours,2)
)

k4.metric(
    "Working Hours",
    round(working_hours,2)
)

st.divider()

# ----------------------------------------------------
# PRODUCTIVITY
# ----------------------------------------------------

productivity = 0

if working_hours > 0:
    productivity = round(
        (focus_hours / working_hours) * 100,
        2
    )

utilization = 0

if working_hours > 0:
    utilization = round(
        ((meeting_hours + focus_hours) / working_hours) * 100,
        2
    )

k5, k6, k7, k8 = st.columns(4)


# Count WFH Days

wfh_days = (
    filtered["WFH"]
    .astype(str)
    .str.strip()
    .str.lower()
    .eq("yes")
    .sum()
)

# Count Office Days

office_days = (
    filtered["WFH"]
    .astype(str)
    .str.strip()
    .str.lower()
    .eq("no")
    .sum()
)

# Count Leave Days

leave_days = (
    filtered["Leave"]
    .astype(str)
    .str.strip()
    .str.lower()
    .eq("yes")
    .sum()
)

# Count Working Days

working_days = (
    filtered["Leave"]
    .astype(str)
    .str.strip()
    .str.lower()
    .eq("no")
    .sum()

)

k5.metric(
    "Productivity",
    f"{productivity}%"
)

k6.metric(
    "Utilization",
    f"{utilization}%"
)

k7.metric(
    "WFH Days",
    wfh_days
)

k8.metric(
    "Leave Days",
    leave_days
)

st.divider()

# ----------------------------------------------------
# DAILY WORKING HOURS
# ----------------------------------------------------

fig = px.line(
    filtered,
    x="Date",
    y="Total_Working_Hours",
    markers=True,
    title="Daily Working Hours"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.divider()

# ----------------------------------------------------
# MEETING VS FOCUS
# ----------------------------------------------------

left, right = st.columns(2)

with left:

    fig = px.bar(
        filtered,
        x="Date",
        y="Meeting_Hours",
        title="Meeting Hours"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with right:

    fig = px.bar(
        filtered,
        x="Date",
        y="Focus_Hours",
        title="Focus Hours"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

st.divider()

# ----------------------------------------------------
# TRAVEL HOURS
# ----------------------------------------------------

left, right = st.columns(2)

with left:

    fig = px.bar(
        filtered,
        x="Date",
        y="Travel_Hours",
        title="Travel Hours"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with right:

    wfh_df = (
    filtered
    .groupby("WFH")
    .size()
    .reset_index(name="Days")
)

wfh_df = (
    filtered["WFH"]
    .astype(str)
    .replace({
        "Yes": "Work From Home",
        "No": "Office"
    })
    .value_counts()
    .reset_index()
)

wfh_df.columns = ["Work Mode", "Days"]

fig = px.bar(
    wfh_df,
    x="Days",
    y="Work Mode",
    orientation="h",
    color="Work Mode",
    title="Work Mode Distribution"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.divider()

# ----------------------------------------------------
# WEEKDAY ANALYSIS
# ----------------------------------------------------

weekday = (
    filtered
    .groupby("Day")["Total_Working_Hours"]
    .mean()
    .reset_index()
)

fig = px.bar(
    weekday,
    x="Day",
    y="Total_Working_Hours",
    color="Day",
    title="Average Working Hours by Day"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.divider()

# ----------------------------------------------------
# DATA TABLE
# ----------------------------------------------------

st.subheader("Calendar Records")

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

best_day = (
    weekday.sort_values(
        "Total_Working_Hours",
        ascending=False
    )
    .iloc[0]["Day"]
)

st.success(
    f"""
Total Working Hours : {working_hours:.2f}

Productivity : {productivity}%

Utilization : {utilization}%

Most Productive Day : {best_day}

Total WFH Days : {wfh_days}

Office Days : {office_days}

Total Leave Days : {leave_days}

Working Days : {working_days}
"""
)