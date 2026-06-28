import streamlit as st


def department_filter(df):

    return st.selectbox(

        "Department",

        ["All"] + sorted(
            df["Department"].dropna().unique().tolist()
        )

    )


def status_filter(df):

    return st.selectbox(

        "Status",

        ["All"] + sorted(
            df["Status"].dropna().unique().tolist()
        )

    )