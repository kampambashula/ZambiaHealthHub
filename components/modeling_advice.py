import streamlit as st

def show_modeling_advice():
    st.header("Modeling & Simulation for Strategic Planning")

    st.markdown("""
    To support policy decisions, consider incorporating these modeling approaches:
    - **System Dynamics Modeling**: To simulate complex interactions between health determinants, resource allocation, and service delivery.
    - **Agent-Based Modeling**: To explore behavioral and population-level impacts of interventions such as vaccination campaigns or health education.
    - **Scenario Analysis**: Model different funding and intervention scenarios to predict outcomes on key health indicators.
    - **Time Series Forecasting**: Use historical health data to forecast disease incidence or mortality trends.
    - **Optimization Models**: For efficient allocation of limited health resources like workforce, medicines, and infrastructure.
    """)

    st.markdown("""
    ---
    *This strategic planning dashboard can be extended to include detailed dashboards per intervention area, real-time data integration, and advanced simulation tools.*
    """)
