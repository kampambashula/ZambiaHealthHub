# acute.py

import streamlit as st
import pandas as pd
import plotly.express as px
from utils.data_loader import load_acute

st.set_page_config(page_title="Acute Respiratory Infection Analysis", layout="wide")

st.title("🌡️ Acute Respiratory Infection (ARI) in Children - Zambia")
st.write("""
This page presents analysis of DHS data on children with symptoms of ARI (Acute Respiratory Infection) in Zambia.  
Filter by year and explore trends and summary statistics.
""")

# Load data
df = load_acute()

# Filter for Zambia only if column exists
if "CountryName" in df.columns: # type: ignore
    df = df[df["CountryName"] == "Zambia"] # type: ignore

# Check if data available after filtering
if df.empty: # type: ignore
    st.warning("No data available for Zambia.")
    st.stop()

# Show raw data option
if st.checkbox("Show Raw Data"):
    st.dataframe(df)

# Select years available
years = sorted(df["SurveyYear"].dropna().unique()) # type: ignore
selected_years = st.multiselect("Select Survey Year(s)", years, default=years)

if not selected_years:
    st.warning("Please select at least one survey year.")
    st.stop()

df_filtered = df[df["SurveyYear"].isin(selected_years)] # type: ignore

# Summary statistics
st.subheader(f"📊 Summary Statistics for Selected Years")
st.write(df_filtered.groupby("SurveyYear")["Value"].describe())

# Indicator list for filtering
indicators = df_filtered["Indicator"].unique()
selected_indicator = st.selectbox("Select Indicator", indicators)

df_indicator = df_filtered[df_filtered["Indicator"] == selected_indicator]

# Plot time series for the indicator
fig = px.line(
    df_indicator,
    x="SurveyYear",
    y="Value",
    markers=True,
    title=f"Trend of '{selected_indicator}' in Zambia",
    labels={"SurveyYear": "Year", "Value": "Value (%)"}
)
st.plotly_chart(fig, use_container_width=True)
