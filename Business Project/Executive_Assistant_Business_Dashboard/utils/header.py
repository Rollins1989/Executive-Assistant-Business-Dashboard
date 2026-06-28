import streamlit as st
from datetime import datetime


def dashboard_header(title):

    left, right = st.columns([3, 1])

    with left:
        st.title(title)

    with right:
        st.markdown("#### Last Updated")
        st.write(datetime.now().strftime("%d %b %Y"))

    st.divider()