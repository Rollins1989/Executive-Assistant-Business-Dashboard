import streamlit as st
from datetime import datetime

def create_sidebar():

    st.sidebar.title("Executive Assistant")

    st.sidebar.markdown("---")

    st.sidebar.subheader("Dashboard")

    st.sidebar.write("Business Intelligence Suite")

    st.sidebar.write("Version 1.0")

    st.sidebar.markdown("---")

    st.sidebar.subheader("User")

    st.sidebar.write("Executive Assistant")

    st.sidebar.write("Department : Management")

    st.sidebar.markdown("---")

    st.sidebar.subheader("System Status")

    st.sidebar.success("Operational")

    st.sidebar.write(
        f"Updated : {datetime.now().strftime('%d %b %Y')}"
    )

    st.sidebar.markdown("---")

    st.sidebar.subheader("Quick Summary")

    st.sidebar.metric("Datasets", 6)

    st.sidebar.metric("Reports", 10)

    st.sidebar.metric("Charts", 25)

    st.sidebar.markdown("---")

    st.sidebar.subheader("Reports")

    st.sidebar.button("Download PDF")

    st.sidebar.button("Download Excel")

    st.sidebar.markdown("---")

    st.sidebar.caption("Developed using Python, Streamlit, Plotly & Excel")