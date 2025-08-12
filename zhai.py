import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import date
from utils.data_loader import load_data
import geopandas as gpd
import numpy as np

st.set_page_config(
    page_title="Health Analytics App",
    layout="wide",
    page_icon="💉"
)

# --- Title & Intro ---
st.title("💊 Zambia Health-Hub Analytics & Insights - ZHAI")
st.markdown(
    f"""
    **Date:** {date.today().strftime("%B %d, %Y")}  
    Welcome to the **Zambia Health-Hub Analytics & Insights Platform** — 
    your gateway to **data-driven insights** for better policy decisions, 
    strategic planning, and effective program monitoring.
    
    ---
    """
)

# --- Load baseline data for KPIs ---
wb_data = load_data("data/worldbank_health_indicators.csv")

# Normalize Year to int if datetime
if pd.api.types.is_datetime64_any_dtype(wb_data['Year']):
    wb_data['Year'] = wb_data['Year'].dt.year

latest_year = wb_data['Year'].max()

def get_latest_value(df, col_name):
    if col_name in df.columns:
        latest_rows = df[df['Year'] == latest_year]
        if not latest_rows.empty:
            val = latest_rows.iloc[0][col_name]
            if pd.isna(val):
                return None
            return val
    return None

# Get latest values safely
health_expenditure = get_latest_value(wb_data, "Current health expenditure (% of GDP)")
fertility_rate = get_latest_value(wb_data, "Fertility rate, total (births per woman)")
life_expectancy_m = get_latest_value(wb_data, "Life expectancy at birth, male (years)")

# Fallbacks if None or NaN
if health_expenditure is None:
    health_expenditure = 5.5  # hardcoded default
if fertility_rate is None:
    fertility_rate = 4.1  # hardcoded default
if life_expectancy_m is None:
    life_expectancy_m = 61.3  # hardcoded default

# --- KPI Summary Cards ---
col1, col2, col3 = st.columns(3)
col1.metric("💰 Current Health Expenditure (% of GDP)", f"{health_expenditure:.2f}%", "↑ 0.3%")
col2.metric("👶 Fertility Rate", f"{fertility_rate:.1f} births/woman", "-0.3%")
col3.metric("⏳ Life Expectancy (Male)", f"{life_expectancy_m:.1f} years", "+0.5%")

# --- Quick Highlights ---
st.subheader("📌 Key Highlights")
st.write(
    """
    - **Disease Surveillance:** Track trends in communicable and non-communicable diseases.
    - **Program Coverage:** Monitor vaccination rates, maternal health, and health facility access.
    - **Resource Allocation:** Optimize distribution of health facilities and healthcare staff.
    """
)

# --- Featured Visuals ---

st.subheader("🗺️ Health Facilities Distribution")
try:
    gdf = gpd.read_file("data/zambia_health_facilities.geojson")
    fig_map = px.scatter_mapbox(
        gdf,
        lat=gdf.geometry.y,
        lon=gdf.geometry.x,
        hover_name="name" if "name" in gdf.columns else None,
        zoom=5,
        height=400,
        title="Health Facilities in Zambia"
    )
    fig_map.update_layout(mapbox_style="open-street-map", margin={"r":0,"t":30,"l":0,"b":0})
    st.plotly_chart(fig_map, use_container_width=True)
except Exception as e:
    st.warning(f"Could not load map data: {e}")


st.markdown("---")
st.info("💡 Navigate to **Program Monitoring**, **Strategic Planning**, or **Policy Simulation** for deeper insights and interactive tools.")
