import streamlit as st
import pandas as pd
import plotly.express as px
from utils.data_loader import load_data, load_dhs_data, load_malaria, load_hiv_prevalence, load_tuberculosis

st.set_page_config(page_title="Analytics - Zambia Health", layout="wide")
st.title("📅 Zambia Health Strategic Analytics")

# Load datasets
DATA_PATH_WB = "data/worldbank_health_indicators.csv"
try:
    df_wb = load_data(DATA_PATH_WB)
except Exception as e:
    st.error(f"Error loading World Bank data: {e}")
    st.stop()

df_dhs = load_dhs_data()
df_malaria = load_malaria()
df_hiv = load_hiv_prevalence()
df_tb = load_tuberculosis()

# Filter World Bank data for Zambia only
if "Country Name" in df_wb.columns:
    df_wb = df_wb[df_wb["Country Name"].str.lower() == "zambia"]

# Parse Year columns consistently
def parse_year_col(df, col="Year"):
    if col in df.columns and not pd.api.types.is_datetime64_any_dtype(df[col]):
        df[col] = pd.to_datetime(df[col], format="%Y", errors="coerce")
    return df

df_wb = parse_year_col(df_wb)
df_dhs = parse_year_col(df_dhs, col="SurveyYear")
df_malaria = parse_year_col(df_malaria, col="YEAR (DISPLAY)")
df_hiv = parse_year_col(df_hiv, col="SurveyYear")
df_tb = parse_year_col(df_tb, col="Year")

# Section 1: Health Expenditure & Life Expectancy from World Bank
st.subheader("Health Expenditure & Life Expectancy Trends (World Bank Data)")

if "Current health expenditure (% of GDP)" in df_wb.columns:
    fig_exp = px.area(
        df_wb,
        x="Year",
        y="Current health expenditure (% of GDP)",
        title="Health Expenditure (% of GDP) Over Time",
        labels={"Year": "Year", "Current health expenditure (% of GDP)": "Health Expenditure (% GDP)"},
    )
    st.plotly_chart(fig_exp, use_container_width=True)
else:
    st.warning("Health expenditure data not available.")

life_cols = [c for c in df_wb.columns if "Life expectancy at birth" in c]
if life_cols:
    fig_life = px.line(
        df_wb,
        x="Year",
        y=life_cols,
        title="Life Expectancy at Birth Over Time",
        labels={"value": "Years", "variable": "Indicator"},
    )
    st.plotly_chart(fig_life, use_container_width=True)
else:
    st.warning("Life expectancy data not available.")

# Section 2: DHS Key Health Indicators Overview
st.subheader("DHS Key Health Indicators")

if not df_dhs.empty:
    indicators = df_dhs["Indicator"].unique()
    selected_indicator = st.selectbox("Select DHS Indicator", indicators)

    dhs_filtered = df_dhs[df_dhs["Indicator"] == selected_indicator]
    if "SurveyYear" in dhs_filtered.columns and "Value" in dhs_filtered.columns:
        fig_dhs = px.line(
            dhs_filtered,
            x="SurveyYear",
            y="Value",
            title=f"{selected_indicator} Trend in Zambia (DHS)",
            labels={"SurveyYear": "Year", "Value": "Value (%)"},
            markers=True,
        )
        st.plotly_chart(fig_dhs, use_container_width=True)
else:
    st.info("DHS data not available.")

# Section 3: Malaria, HIV, Tuberculosis Disease Burden (DHS + Disease Data)
st.subheader("Communicable Diseases Trends")

# Malaria cases and mortality
if not df_malaria.empty and "Numeric" in df_malaria.columns:
    df_malaria_zmb = df_malaria[df_malaria["COUNTRY (DISPLAY)"].str.lower() == "zambia"]
    if not df_malaria_zmb.empty:
        fig_malaria = px.line(
            df_malaria_zmb,
            x="YEAR (DISPLAY)",
            y="Numeric",
            color="GHO (DISPLAY)",
            title="Malaria Indicators in Zambia",
            labels={"YEAR (DISPLAY)": "Year", "Numeric": "Value"},
            markers=True,
        )
        st.plotly_chart(fig_malaria, use_container_width=True)

# HIV prevalence (from DHS or hiv data)
if not df_hiv.empty and "Value" in df_hiv.columns:
    hiv_indicators = df_hiv["Indicator"].unique()
    selected_hiv = st.selectbox("Select HIV Indicator", hiv_indicators)
    hiv_filtered = df_hiv[df_hiv["Indicator"] == selected_hiv]
    if not hiv_filtered.empty:
        fig_hiv = px.line(
            hiv_filtered,
            x="SurveyYear",
            y="Value",
            title=f"HIV Indicator: {selected_hiv}",
            labels={"SurveyYear": "Year", "Value": "Value (%)"},
            markers=True,
        )
        st.plotly_chart(fig_hiv, use_container_width=True)

# Tuberculosis incidence
if not df_tb.empty and "Value" in df_tb.columns:
    tb_indicators = df_tb["GHO (DISPLAY)"].unique()
    selected_tb = st.selectbox("Select Tuberculosis Indicator", tb_indicators)
    tb_filtered = df_tb[df_tb["GHO (DISPLAY)"] == selected_tb]
    if not tb_filtered.empty:
        fig_tb = px.line(
            tb_filtered,
            x="YEAR (DISPLAY)",
            y="Value",
            title=f"Tuberculosis Indicator: {selected_tb}",
            labels={"Year": "Year", "Value": "Value per 100,000"},
            markers=True,
        )
        st.plotly_chart(fig_tb, use_container_width=True)

# Strategic Context Summary
st.markdown("""
---
### Strategic Planning Context: Zambia National Health Plan 2022-2026

- **Primary Health Care:** Strengthen PHC towards Universal Health Coverage by 2030.
- **Maternal & Child Health:** Reduce maternal mortality to <100/100,000 live births; under-five mortality to 25/1000 by 2026.
- **Communicable Diseases:** Reduce malaria incidence from 340 to 201 per 1000; HIV incidence and TB incidence significantly lowered by 2026.
- **Non-Communicable Diseases:** Reduce premature mortality by 30% by 2026.
- **Health Workforce:** Increase health worker ratios for better coverage.
- **Health Financing:** Increase sustainable health sector financing aiming for Abuja target of 15% of national budget.

Monitoring these data streams allows tracking progress on Zambia Vision 2030 and SDG3.

""")
