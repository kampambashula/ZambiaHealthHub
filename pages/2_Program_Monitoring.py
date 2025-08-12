import streamlit as st
import pandas as pd
import plotly.express as px
from utils.data_loader import load_data

st.set_page_config(page_title="Strategic Planning", layout="wide")
st.title("📅 Strategic Planning Insights")

DATA_PATH = "data/worldbank_health_indicators.csv"

try:
    df = load_data(DATA_PATH)
except Exception as e:
    st.error(f"Error loading data: {e}")
    st.stop()

st.subheader("Health Expenditure and Life Expectancy Trends")

# Example: Current health expenditure (% of GDP) over years
if "Current health expenditure (% of GDP)" in df.columns:
    fig = px.area(
        df,
        x="Year",
        y="Current health expenditure (% of GDP)",
        title="Current Health Expenditure (% of GDP) Over Time",
        labels={"Year": "Year", "Current health expenditure (% of GDP)": "Health Expenditure (% GDP)"},
    )
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("Health expenditure column not found in data.")

# Example: Life expectancy at birth (male)
if "Life expectancy at birth, male (years)" in df.columns:
    fig2 = px.line(
        df,
        x="Year",
        y="Life expectancy at birth, male (years)",
        title="Life Expectancy at Birth (Male) Over Time",
        labels={"Year": "Year", "Life expectancy at birth, male (years)": "Life Expectancy (Years)"},
    )
    st.plotly_chart(fig2, use_container_width=True)
else:
    st.warning("Life expectancy column not found in data.")
