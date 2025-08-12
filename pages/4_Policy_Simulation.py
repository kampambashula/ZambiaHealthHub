# policy_simulation.py

import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
from utils.data_loader import load_data

@st.cache_data
def load_baseline_health_data():
    """
    Load baseline health indicators from World Bank dataset or similar.
    Returns latest year, life expectancy, under-5 mortality rate.
    """
    df = load_data("data/worldbank_health_indicators.csv")
    if df.empty:
        st.warning("Baseline health data not available.")
        return 64, 61, 2020  # fallback default baseline values
    
    latest_year = df['Year'].max()
    
    # Ensure latest_year is an int, not Timestamp
    if hasattr(latest_year, "year"):
        latest_year = latest_year.year
    
    # Use columns likely available in your dataset; adjust if needed
    le_col = 'Life expectancy at birth, total (years)'
    u5mr_col = 'Mortality rate, under-5 (per 1000 live births)'
    
    if le_col in df.columns and u5mr_col in df.columns:
        life_expectancy = df.loc[df['Year'] == pd.to_datetime(str(latest_year)), le_col].values[0]
        u5_mortality = df.loc[df['Year'] == pd.to_datetime(str(latest_year)), u5mr_col].values[0]
        return life_expectancy, u5_mortality, latest_year
    
    # Defaults if columns missing
    return 64, 61, latest_year

def simulate_policy_impact(
    budget_million,
    hospital_pct,
    staff_increase_pct,
    vacc_coverage_pct,
    hiv_art_pct,
    malaria_coverage_pct,
    tb_treatment_pct,
    base_life_exp,
    base_u5_mortality,
):
    """
    Simple weighted model to simulate policy impact on life expectancy and under-5 mortality.
    """
    life_exp_gain = (
        (budget_million / 5000) * 2 +
        (staff_increase_pct / 50) * 1.5 +
        ((vacc_coverage_pct - 80) / 20) * 1 +
        (hiv_art_pct - 70) * 0.05 +
        (malaria_coverage_pct - 70) * 0.05 +
        (tb_treatment_pct - 80) * 0.05
    )
    mortality_drop = (
        (budget_million / 5000) * 1 +
        (staff_increase_pct / 50) * 1.2 +
        ((vacc_coverage_pct - 80) / 20) * 0.8 +
        (hiv_art_pct - 70) * 0.04 +
        (malaria_coverage_pct - 70) * 0.04 +
        (tb_treatment_pct - 80) * 0.04
    )

    projected_life_exp = base_life_exp + life_exp_gain
    projected_u5_mortality = max(0, base_u5_mortality - mortality_drop)

    return projected_life_exp, projected_u5_mortality, life_exp_gain, mortality_drop

def run_simulation():
    st.header("🛠️ Health Policy Simulation for Zambia")
    st.markdown("""
    Adjust the sliders to explore potential impacts of different health policy decisions on key health outcomes.
    """)

    # Load baseline data
    base_life_exp, base_u5_mortality, base_year = load_baseline_health_data()
    st.markdown(f"**Baseline data from year {base_year}:**")
    st.write(f"- Life Expectancy: {base_life_exp:.1f} years")
    st.write(f"- Under-5 Mortality Rate: {base_u5_mortality:.1f} per 1000 live births")

    # Inputs
    budget = st.slider("Total Annual Health Budget (Million ZMW)", 500, 5000, 2000, step=100)
    hospital_share = st.slider("Budget Share to Hospitals (%)", 20, 80, 50, step=5)
    staff_increase = st.slider("Increase in Healthcare Staff (%)", 0, 50, 10, step=5)
    vaccination_coverage = st.slider("Vaccination Coverage (%)", 50, 100, 80, step=5)
    hiv_art_coverage = st.slider("HIV ART Coverage (%)", 40, 100, 75, step=5)
    malaria_coverage = st.slider("Malaria Prevention Coverage (%)", 40, 100, 70, step=5)
    tb_treatment_success = st.slider("TB Treatment Success Rate (%)", 50, 100, 85, step=5)

    # Run simulation model
    proj_life_exp, proj_u5_mort, gain_life_exp, drop_mort = simulate_policy_impact(
        budget, hospital_share, staff_increase, vaccination_coverage,
        hiv_art_coverage, malaria_coverage, tb_treatment_success,
        base_life_exp, base_u5_mortality,
    )

    # Show metrics
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Projected Life Expectancy", f"{proj_life_exp:.1f} years", f"{gain_life_exp:+.2f} yrs change")
    with col2:
        st.metric("Projected Under-5 Mortality Rate", f"{proj_u5_mort:.2f} per 1000", f"{-drop_mort:.2f} change")

    # Time projections over next 10 years
    years = np.arange(base_year, base_year + 11)
    life_exp_proj = base_life_exp + np.cumsum(np.repeat(gain_life_exp / 10, 11))
    u5_mort_proj = base_u5_mortality - np.cumsum(np.repeat(drop_mort / 10, 11))
    u5_mort_proj = np.clip(u5_mort_proj, 0, None)

    df_proj = pd.DataFrame({
        "Year": years,
        "Life Expectancy": life_exp_proj,
        "Under-5 Mortality Rate": u5_mort_proj,
    })

    fig = px.line(
        df_proj,
        x="Year",
        y=["Life Expectancy", "Under-5 Mortality Rate"],
        title="📈 Projected Policy Impact Over Time",
        labels={"value": "Metric", "variable": "Indicator"},
    )
    st.plotly_chart(fig, use_container_width=True)

    # Summary text
    st.subheader("Summary & Insights")
    st.write(
        f"""
        With a total annual budget of **{budget} million ZMW**, allocating **{hospital_share}%** to hospitals, 
        increasing healthcare staff by **{staff_increase}%**, and achieving:
        - Vaccination coverage of **{vaccination_coverage}%**
        - HIV ART coverage of **{hiv_art_coverage}%**
        - Malaria prevention coverage of **{malaria_coverage}%**
        - TB treatment success rate of **{tb_treatment_success}%**

        Zambia can expect to see:
        - An increase in life expectancy to **{proj_life_exp:.1f} years** over the next decade.
        - A reduction in under-5 mortality rate to **{proj_u5_mort:.2f} deaths per 1000 live births**.
        """
    )

if __name__ == "__main__":
    run_simulation()
