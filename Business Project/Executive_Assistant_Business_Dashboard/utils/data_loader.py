import pandas as pd
import os
import streamlit as st

project_folder = os.path.dirname(os.path.dirname(__file__))
data_folder = os.path.join(project_folder, "data")


@st.cache_data
def load_data():

    data = {}

    files = {
        "meetings": "meetings.xlsx",
        "tasks": "tasks.xlsx",
        "followups": "followups.xlsx",
        "vendors": "vendors.xlsx",
        "expenses": "expenses.xlsx",
        "calendar": "calendar.xlsx",
    }

    for key, file in files.items():
        path = os.path.join(data_folder, file)
        data[key] = pd.read_excel(path)

    return data