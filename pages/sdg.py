# sdg.py

import streamlit as st
import pandas as pd
import plotly.express as px

# Page title and description
st.title("🌍 SDG Health Targets Analysis")
st.write("""
This page provides analysis of Sustainable Development Goal (SDG) health indicators  
based on DHS datasets. You can filter by survey year, indicator, and view trends over time.
""")

# Load CSV
file_path = "data/sdgs_national_zmb.csv"
try:
    df = pd.read_csv(file_path)
except FileNotFoundError:
    st.error(f"CSV file not found at {file_path}. Please ensure it is in the correct folder.")
    st.stop()

# Optional raw data view
if st.checkbox("Show Raw Data"):
    st.dataframe(df)

# Filter by country
countries = sorted(df["CountryName"].unique())
selected_country = st.selectbox("Select Country", countries)
df_country = df[df["CountryName"] == selected_country]

# Filter by year
years = sorted(df_country["SurveyYear"].unique())
selected_year = st.selectbox("Select Survey Year", years)
df_year = df_country[df_country["SurveyYear"] == selected_year]


# Bar chart for selected year
st.subheader("📈 Indicator Values for Selected Year")
fig = px.bar(
    df_year,
    x="Indicator",
    y="Value",
    color="Indicator",
    title=f"SDG Health Indicators in {selected_year} - {selected_country}",
    labels={"Value": "Value", "Indicator": "Indicator"},
)
fig.update_layout(xaxis_tickangle=45)
st.plotly_chart(fig, use_container_width=True)

# Time series trend for selected indicator
st.subheader("⏳ Trends Over Time")
indicator_choice = st.selectbox("Select Indicator", df_country["Indicator"].unique())
df_indicator = df_country[df_country["Indicator"] == indicator_choice]

fig2 = px.line(
    df_indicator,
    x="SurveyYear",
    y="Value",
    markers=True,
    title=f"Trend of {indicator_choice} in {selected_country} Over Time",
    labels={"Value": "Value", "SurveyYear": "Year"},
)
st.plotly_chart(fig2, use_container_width=True)
