import streamlit as st
import pandas as pd
import plotly.express as px
import os
from utils.data_loader import load_covid_data

# --- Page Setup ---
st.title("🦠 COVID Prevention & Health Infrastructure Analysis")

# --- Load Data ---
path = "data/covid-19-prevention_national_zmb.csv"
df = load_covid_data()

# --- Show Data Preview ---
st.subheader("Dataset Preview")
st.dataframe(df.head())

# --- Country Filter ---
countries = df["CountryName"].dropna().unique()
selected_country = st.selectbox("Select a Country", sorted(countries))

country_df = df[df["CountryName"] == selected_country]

# --- Indicator Filter ---
indicators = country_df["Indicator"].dropna().unique()
selected_indicator = st.selectbox("Select an Indicator", sorted(indicators))

indicator_df = country_df[country_df["Indicator"] == selected_indicator]

# --- Trend Chart ---
st.subheader(f"Trend for '{selected_indicator}' in {selected_country}")
fig_trend = px.line(
    indicator_df,
    x="SurveyYear",
    y="Value",
    title=f"{selected_indicator} Over Time in {selected_country}",
    markers=True,
    labels={"Value": "Value (%)", "SurveyYear": "Year"}
)
st.plotly_chart(fig_trend, use_container_width=True)

# --- Regional Comparison ---
st.subheader(f"Regional Comparison ({selected_indicator})")
latest_year = indicator_df["SurveyYear"].max()
latest_df = df[(df["SurveyYear"] == latest_year) & (df["Indicator"] == selected_indicator)]

fig_region = px.bar(
    latest_df,
    x="CountryName",
    y="Value",
    title=f"{selected_indicator} in {latest_year} (All Countries)",
    labels={"Value": "Value (%)", "CountryName": "Country"}
)
st.plotly_chart(fig_region, use_container_width=True)

# --- Notes ---
st.info("💡 This page focuses on analyzing public health indicators relevant to COVID-19 prevention, "
        "such as access to water, sanitation, and health infrastructure.")
