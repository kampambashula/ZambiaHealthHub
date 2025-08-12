# immunization.py

import streamlit as st
import pandas as pd
import plotly.express as px
from utils.data_loader import load_immunization

# Page title and description
st.title("💉 Immunization Analysis")
st.write("""
This section provides insights into immunization coverage based on DHS survey data.  
It allows filtering by survey year and analyzing trends over time.
""")

# Load the CSV file
df = load_immunization()

# Show raw data option
if st.checkbox("Show Raw Data"):
    st.dataframe(df)

# Filter by year
years = sorted(df["SurveyYear"].unique())
selected_year = st.selectbox("Select Survey Year", years)

df_year = df[df["SurveyYear"] == selected_year]

# Summary statistics
st.subheader(f"📊 Summary for {selected_year}")
st.write(df_year.groupby("Indicator")["Value"].describe())

# Plot immunization rates
st.subheader("📈 Immunization Coverage Trends")
fig = px.bar(
    df_year,
    x="Indicator",
    y="Value",
    color="Indicator",
    title=f"Immunization Indicators in {selected_year}",
    labels={"Value": "Coverage (%)", "Indicator": "Immunization Type"},
)
fig.update_layout(xaxis_tickangle=45)
st.plotly_chart(fig, use_container_width=True)

# Time series trend for all years
st.subheader("⏳ Trends Over Time")
indicator_choice = st.selectbox("Select Immunization Indicator", df["Indicator"].unique())

df_indicator = df[df["Indicator"] == indicator_choice]
fig2 = px.line(
    df_indicator,
    x="SurveyYear",
    y="Value",
    markers=True,
    title=f"Trend of {indicator_choice} Over Time",
    labels={"Value": "Coverage (%)", "SurveyYear": "Year"},
)
st.plotly_chart(fig2, use_container_width=True)
