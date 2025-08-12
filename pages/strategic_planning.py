import streamlit as st
from components import summary, indicators, interventions, modeling_advice, simulation


st.set_page_config(page_title="Strategic Health Planning", layout="wide", page_icon="📈")

st.title("🩺 Zambia National Health Strategic Plan 2022-2026")
st.markdown("""
This dashboard supports health policy makers to analyze, plan, and simulate Zambia’s health sector progress
aligned with the National Health Strategic Plan 2022-2026, Zambia Vision 2030, and Sustainable Development Goals (SDGs).
""")

# Show summary
summary.show_summary()

# Load indicator data
data_file = "data/worldbank_health_indicators.csv"  # Replace with your actual data path
try:
    df = indicators.load_indicator_data(data_file)
    indicators.show_indicators(df)
except Exception as e:
    st.error(f"Error loading indicator data: {e}")

# Run your modular simulation function here
simulation.run_simulation()

# Other sections
interventions.show_interventions()
modeling_advice.show_modeling_advice()
