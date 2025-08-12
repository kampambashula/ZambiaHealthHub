# pages/dhs.py

import streamlit as st
import pandas as pd
import plotly.express as px
from utils.data_loader import load_dhs_data

st.set_page_config(page_title="DHS Data Analysis", layout="wide")

st.title("📑 DHS Survey Data Analysis")
st.markdown(
    """
    This page provides an interactive analysis of the DHS survey data.  
    Use filters to explore specific indicators, years, and demographics.
    """
)



df = load_dhs_data()

if not df.empty:
    # Show raw data toggle
    if st.checkbox("Show raw DHS data"):
        st.dataframe(df)

    # --- Filters ---
    indicators = df["Indicator"].dropna().unique()
    selected_indicator = st.selectbox("Select Indicator", sorted(indicators))

    years = df["SurveyYear"].dropna().unique()
    selected_years = st.multiselect("Select Years", sorted(years), default=sorted(years))

    # Filtered Data
    filtered_df = df[
        (df["Indicator"] == selected_indicator) &
        (df["SurveyYear"].isin(selected_years))
    ]

    # --- Visualizations ---
    if not filtered_df.empty:
        st.subheader(f"Trend for: {selected_indicator}")

        fig = px.line(
            filtered_df,
            x="SurveyYear",
            y="Value",
            color="CharacteristicLabel",
            markers=True,
            title=f"{selected_indicator} by Year",
            labels={"Value": "Percentage", "SurveyYear": "Year"}
        )
        st.plotly_chart(fig, use_container_width=True)

        # Summary stats
        st.subheader("Summary Statistics")
        st.write(filtered_df.groupby("SurveyYear")["Value"].describe())
    else:
        st.warning("No data available for the selected filters.")
