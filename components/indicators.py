import streamlit as st
import plotly.graph_objects as go
import pandas as pd

def load_indicator_data(file_path):
    df = pd.read_csv(file_path)
    # Filter Zambia data and relevant columns
    
    return df

def show_indicators(df):
    st.header("Progress on Key Health Indicators")

    # Filter key indicators (customize based on data)
    key_indicators = [
        "Contraceptive Prevalence Rate (%)",
        "Under-5 Mortality Rate (per 1000 live births)",
        "Infant Mortality Rate (per 1000 live births)",
        "Malaria Incidence (cases per 1000 population)",
        "HIV Incidence (new cases)",
        "TB Incidence (per 100,000 population)"
    ]

    # For this example, build mock data based on previous hardcoded or from df
    indicators = {
        "Contraceptive Prevalence Rate (%)": {"2014": 45, "2018": 50, "Target 2026": 60},
        "Under-5 Mortality Rate (per 1000 live births)": {"2013": 75, "2018": 61, "Target 2026": 25},
        "Infant Mortality Rate (per 1000 live births)": {"2013": 45, "2018": 42, "Target 2026": 15},
        "Malaria Incidence (cases per 1000 population)": {"2021": 340, "Target 2026": 201},
        "HIV Incidence (new cases)": {"Current": 28000, "Target 2026": 15000},
        "TB Incidence (per 100,000 population)": {"2016": 376, "2021": 319, "Target 2026": 169}
    }

    # Plot indicators with plotly
    fig = go.Figure()
    years = sorted({year for vals in indicators.values() for year in vals.keys()})

    for ind, vals in indicators.items():
        x = []
        y = []
        for yr in years:
            x.append(str(yr))
            y.append(vals.get(yr, None))
        fig.add_trace(go.Scatter(x=x, y=y, mode='lines+markers', name=ind))

    fig.update_layout(
        title="Trends and Targets for Key Health Indicators",
        xaxis_title="Year",
        yaxis_title="Value",
        hovermode="x unified",
        height=450
    )
    st.plotly_chart(fig, use_container_width=True)
