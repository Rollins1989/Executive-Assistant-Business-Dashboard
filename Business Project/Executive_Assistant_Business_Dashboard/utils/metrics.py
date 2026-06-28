import streamlit as st


def kpi_card(title, value, color="#2563EB"):

    st.markdown(
        f"""
        <div style="
            background-color:white;
            padding:20px;
            border-radius:15px;
            border-left:6px solid {color};
            box-shadow:0px 4px 12px rgba(0,0,0,0.12);
            margin-bottom:15px;
        ">

        <p style="
            font-size:15px;
            color:#666666;
            margin-bottom:10px;
        ">
        {title}
        </p>

        <h2 style="
            color:#111827;
            margin:0;
        ">
        {value}
        </h2>

        </div>
        """,
        unsafe_allow_html=True
    )