import streamlit as st
import pandas as pd
import plotly.express as px
from utils.data_loader import load_data

st.set_page_config(page_title="Main Dashboard", layout="wide")
st.title("📈 Main Health Dashboard")

# Load health indicators CSV
DATA_PATH = "data/worldbank_health_indicators.csv"

try:
    df = load_data(DATA_PATH)
except Exception as e:
    st.error(f"Error loading data: {e}")
    st.stop()

st.subheader("Overview of Key Health Indicators Over Time")

# Example plot: Infant Mortality Rate over years
if "Mortality rate, infant, male (per 1,000 live births)" in df.columns:
    fig = px.line(
        df,
        x="Year",
        y="Mortality rate, infant, male (per 1,000 live births)",
        title="Infant Mortality Rate (Male) Over Time",
        labels={"Year": "Year", "Mortality rate, infant, male (per 1,000 live births)": "Infant Mortality Rate (per 1000 live births)"},
    )
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("Infant mortality rate column not found in data.")

# Add other key indicator plots similarly...
