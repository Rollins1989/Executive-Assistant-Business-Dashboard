import streamlit as st
import os


def load_css():

    css_path = os.path.join(
        "assets",
        "style.css"
    )

    if os.path.exists(css_path):

        with open(css_path) as f:

            st.markdown(
                f"<style>{f.read()}</style>",
                unsafe_allow_html=True
            )