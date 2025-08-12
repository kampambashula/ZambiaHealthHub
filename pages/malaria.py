# malaria.py

import streamlit as st
import pandas as pd
import plotly.express as px
import os
from utils.data_loader import load_malaria

# --- Page Config ---
st.set_page_config(page_title="Malaria Data Analysis - Zambia", page_icon="🦟", layout="wide")

# --- Page Title ---
st.title("🦟 Malaria Data Analysis - Zambia")
st.markdown("This dashboard analyses malaria-related statistics for **Zambia** from the WHO Global Health Observatory.")

# --- Load Data ---
df = load_malaria()

# --- Filter for Zambia only ---
if "COUNTRY (DISPLAY)" in df.columns:
    df = df[df["COUNTRY (DISPLAY)"] == "Zambia"]

# --- Data Overview ---
with st.expander("📄 View Raw Zambia Data"):
    st.dataframe(df)

# --- Yearly Trend of Malaria Mortality ---
if "YEAR (DISPLAY)" in df.columns and "Numeric" in df.columns:
    fig_trend = px.line(
        df,
        x="YEAR (DISPLAY)",
        y="Numeric",
        color="GHO (DISPLAY)",
        title="Trend of Malaria Indicators in Zambia Over Time",
        markers=True
    )
    fig_trend.update_layout(yaxis_title="Value", xaxis_title="Year")
    st.plotly_chart(fig_trend, use_container_width=True)

# --- Value Distribution ---
if "Numeric" in df.columns:
    fig_hist = px.histogram(
        df,
        x="Numeric",
        nbins=20,
        title="Distribution of Malaria Indicator Values in Zambia",
        marginal="box"
    )
    st.plotly_chart(fig_hist, use_container_width=True)

# --- Download Zambia Data ---
st.download_button(
    label="📥 Download Zambia Malaria Data as CSV",
    data=df.to_csv(index=False),
    file_name="malaria_zambia.csv",
    mime="text/csv"
)
