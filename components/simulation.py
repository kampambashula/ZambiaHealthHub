import streamlit as st
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from utils.data_loader import load_data, load_malaria

def run_simulation():
    st.header("Interactive Simulation: RMNCAH-N Indicator Progress")

    st.markdown("Simulate yearly progress to 2026 targets for Under-5 Mortality Rate and Contraceptive Prevalence Rate.")

    # RMNCAH-N simulation (your original)
    u5mr_start = st.slider("Under-5 Mortality Rate (per 1000) in 2018", 20, 100, 61)
    u5mr_target = 25
    u5mr_years = 2026 - 2018

    contr_prev_start = st.slider("Contraceptive Prevalence Rate (%) in 2018", 30, 60, 50)
    contr_prev_target = 60

    # Calculate yearly linear progress for RMNCAH-N
    u5mr_yearly = np.linspace(u5mr_start, u5mr_target, u5mr_years + 1)
    contr_prev_yearly = np.linspace(contr_prev_start, contr_prev_target, u5mr_years + 1)
    years_sim = list(range(2018, 2027))

    fig_sim = go.Figure()
    fig_sim.add_trace(go.Scatter(x=years_sim, y=u5mr_yearly, mode='lines+markers', name='Under-5 Mortality Rate'))
    fig_sim.add_trace(go.Scatter(x=years_sim, y=contr_prev_yearly, mode='lines+markers', name='Contraceptive Prevalence Rate'))
    fig_sim.update_layout(
        title="Simulated Progress to 2026 Targets",
        xaxis_title="Year",
        yaxis_title="Value",
        height=400
    )
    st.plotly_chart(fig_sim, use_container_width=True)

    st.markdown("---")
    # === Malaria ===
    st.header("Malaria Incidence Rate Projection and Simulation")

    malaria_path = "data/malaria_indicators_zmb.csv"
    try:
        df_malaria = load_malaria()
        df_malaria = df_malaria[["YEAR (DISPLAY)", "Numeric"]].dropna()
        df_malaria = df_malaria.sort_values("YEAR (DISPLAY)")
    except Exception as e:
        st.error(f"Failed to load malaria data: {e}")
        return

    fig_malaria = px.line(
        df_malaria,
        x="YEAR (DISPLAY)",
        y="Numeric",
        title="Malaria Incidence Rate Over Time - Zambia",
        labels={"YEAR (DISPLAY)": "Year", "Numeric": "Incidence per 1000"}
    )
    st.plotly_chart(fig_malaria, use_container_width=True)

    annual_reduction_malaria = st.slider("Annual Reduction Rate for Malaria Incidence (%)", 0.0, 20.0, 5.0, step=0.1)
    last_year_malaria = int(df_malaria["YEAR (DISPLAY)"].max())
    last_value_malaria = df_malaria.loc[df_malaria["YEAR (DISPLAY)"] == last_year_malaria, "Numeric"].values[0]

    years_future_malaria = list(range(last_year_malaria + 1, 2027))
    projected_values_malaria = [last_value_malaria * ((1 - annual_reduction_malaria / 100) ** i) for i in range(1, len(years_future_malaria) + 1)]

    fig_proj_malaria = go.Figure()
    fig_proj_malaria.add_trace(go.Scatter(x=years_future_malaria, y=projected_values_malaria, mode='lines+markers', name='Projected Malaria Incidence'))
    fig_proj_malaria.update_layout(
        title=f"Malaria Incidence Projection with {annual_reduction_malaria}% Annual Reduction",
        xaxis_title="Year",
        yaxis_title="Incidence per 1000",
        height=400
    )
    st.plotly_chart(fig_proj_malaria, use_container_width=True)

    st.markdown("---")
    # === HIV ===
    st.header("HIV Incidence Projection and Simulation")

    hiv_path = "data/hiv-prevalence_national_zmb.csv"
    try:
        df_hiv = load_data(hiv_path)
        # Assuming columns like 'Year' and 'Value' or similar, adjust if necessary
        # Check your CSV column names and adjust below:
        if "SurveyYear" in df_hiv.columns and "Value" in df_hiv.columns:
            df_hiv = df_hiv[["SurveyYear", "Value"]].dropna().sort_values("SurveyYear")
        else:
            st.warning("HIV data columns 'Year' or 'Value' not found.")
            return
    except Exception as e:
        st.error(f"Failed to load HIV data: {e}")
        return

    fig_hiv = px.line(
        df_hiv,
        x="SurveyYear",
        y="Value",
        title="HIV Incidence Over Time - Zambia",
        labels={"Year": "Year", "Value": "Incidence"}
    )
    st.plotly_chart(fig_hiv, use_container_width=True)

    annual_reduction_hiv = st.slider("Annual Reduction Rate for HIV Incidence (%)", 0.0, 20.0, 3.0, step=0.1)
    last_year_hiv = int(df_hiv["SurveyYear"].max())
    last_value_hiv = df_hiv.loc[df_hiv["SurveyYear"] == last_year_hiv, "Value"].values[0]

    years_future_hiv = list(range(last_year_hiv + 1, 2027))
    projected_values_hiv = [last_value_hiv * ((1 - annual_reduction_hiv / 100) ** i) for i in range(1, len(years_future_hiv) + 1)]

    fig_proj_hiv = go.Figure()
    fig_proj_hiv.add_trace(go.Scatter(x=years_future_hiv, y=projected_values_hiv, mode='lines+markers', name='Projected HIV Incidence'))
    fig_proj_hiv.update_layout(
        title=f"HIV Incidence Projection with {annual_reduction_hiv}% Annual Reduction",
        xaxis_title="SurveyYear",
        yaxis_title="Incidence",
        height=400
    )
    st.plotly_chart(fig_proj_hiv, use_container_width=True)

    st.markdown("---")
# === Tuberculosis ===
st.header("Tuberculosis Incidence Projection and Simulation")

tb_path = "data/tuberculosis_indicators_zmb.csv"
try:
    df_tb = load_data(tb_path)
    # Adjust column names here to your dataset; assuming 'YEAR (DISPLAY)' and 'Value'
    if "YEAR (DISPLAY)" in df_tb.columns and "Value" in df_tb.columns:
        df_tb = df_tb[["YEAR (DISPLAY)", "Value"]].dropna().sort_values("YEAR (DISPLAY)")
    else:
        st.warning("TB data columns 'YEAR (DISPLAY)' or 'Value' not found.")
        st.stop()
except Exception as e:
    st.error(f"Failed to load Tuberculosis data: {e}")
    st.stop()

# Ensure Value is numeric
    df_tb["Value"] = pd.to_numeric(df_tb["Value"], errors="coerce")
    df_tb = df_tb.dropna(subset=["Value"])

    fig_tb = px.line(
        df_tb,
        x="YEAR (DISPLAY)",
        y="Value",
        title="Tuberculosis Incidence Over Time - Zambia",
        labels={"YEAR (DISPLAY)": "Year", "Value": "Incidence per 100,000"}
    )
    st.plotly_chart(fig_tb, use_container_width=True)

    annual_reduction_tb = st.slider(
        "Annual Reduction Rate for TB Incidence (%)", 
        0.0, 20.0, 4.0, step=0.1
    )
    last_year_tb = int(df_tb["YEAR (DISPLAY)"].max())
    last_value_tb = float(
        df_tb.loc[df_tb["YEAR (DISPLAY)"] == last_year_tb, "Value"].values[0]
    )

    years_future_tb = list(range(last_year_tb + 1, 2027))
    projected_values_tb = [
        last_value_tb * ((1 - annual_reduction_tb / 100) ** i)
        for i in range(1, len(years_future_tb) + 1)
    ]

    fig_proj_tb = go.Figure()
    fig_proj_tb.add_trace(go.Scatter(
        x=years_future_tb, 
        y=projected_values_tb, 
        mode='lines+markers', 
        name='Projected TB Incidence'
    ))
    fig_proj_tb.update_layout(
        title=f"Tuberculosis Incidence Projection with {annual_reduction_tb}% Annual Reduction",
        xaxis_title="Year",
        yaxis_title="Incidence per 100,000",
        height=400
    )
    st.plotly_chart(fig_proj_tb, use_container_width=True)

