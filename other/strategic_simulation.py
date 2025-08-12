# strategic_simulation.py
import numpy as np
import pandas as pd
import plotly.express as px
from sklearn.linear_model import LinearRegression
import streamlit as st


def linear_projection(years, values, future_years=5):
    """
    Fit a linear regression on historical data and project values forward.

    Args:
        years (array-like): Historical years.
        values (array-like): Corresponding indicator values.
        future_years (int): Number of years to project forward.

    Returns:
        proj_years (np.array): Projected years.
        proj_values (np.array): Predicted values for projected years.
    """
    mask = (~pd.isna(years)) & (~pd.isna(values))
    x = years[mask].values.reshape(-1, 1)
    y = values[mask].values
    if len(x) < 2:
        return None, None

    model = LinearRegression()
    model.fit(x, y)

    last_year = int(np.max(x))
    proj_years = np.arange(last_year + 1, last_year + 1 + future_years)
    proj_values = model.predict(proj_years.reshape(-1, 1))
    return proj_years, proj_values


def simulate_annual_reduction(last_year, last_value, annual_reduction_rate, years=5):
    """
    Simulate future values by applying a constant annual percentage reduction.

    Args:
        last_year (int): Last known year of data.
        last_value (float): Last known value.
        annual_reduction_rate (float): Annual reduction percentage (e.g., 5 for 5%).
        years (int): Number of years to simulate forward.

    Returns:
        sim_years (np.array): Simulated years.
        sim_values (list): Simulated values after annual reductions.
    """
    sim_years = np.arange(last_year + 1, last_year + 1 + years)
    sim_values = []
    current_value = last_value

    for _ in range(years):
        current_value *= (1 - annual_reduction_rate / 100)
        sim_values.append(current_value)

    return sim_years, sim_values


def plot_trend_with_projection(df, year_col, value_col, title, targets=None, projection_years=5):
    """
    Plot historical data with linear projection and target markers.

    Args:
        df (pd.DataFrame): DataFrame containing historical data.
        year_col (str): Name of the year column.
        value_col (str): Name of the value column.
        title (str): Plot title.
        targets (dict): Optional dict {year: target_value} to plot target markers.
        projection_years (int): Number of years to project forward.

    Returns:
        fig: Plotly figure object.
    """
    fig = px.line(df, x=year_col, y=value_col, markers=True, title=title)

    proj_years, proj_values = linear_projection(df[year_col], df[value_col], future_years=projection_years)
    if proj_years is not None:
        fig.add_scatter(x=proj_years, y=proj_values, mode="lines+markers",
                        name="Projection", line=dict(dash="dash", color="orange"))

    if targets:
        for target_year, target_val in targets.items():
            fig.add_scatter(x=[target_year], y=[target_val], mode="markers+text",
                            name="Target",
                            text=[f"Target: {target_val}"],
                            textposition="top center",
                            marker=dict(symbol="star", size=12, color="red"))

    return fig


def interactive_malaria_simulation(df_malaria, annual_reduction_rate=5.0, simulation_years=5, target_year=2026, target_value=201):
    """
    Create an interactive Streamlit simulation for malaria incidence reduction.

    Args:
        df_malaria (pd.DataFrame): Malaria data filtered for Zambia with columns ['YEAR (DISPLAY)', 'Numeric'].
        annual_reduction_rate (float): Annual reduction rate (%) to simulate.
        simulation_years (int): Number of years to simulate.
        target_year (int): Year of national target.
        target_value (float): Target malaria incidence value.

    Displays:
        Streamlit plot with historical data, simulation, and target marker.
    """
    df_malaria = df_malaria.sort_values("YEAR (DISPLAY)")
    last_year = df_malaria["YEAR (DISPLAY)"].max()
    last_value = df_malaria.loc[df_malaria["YEAR (DISPLAY)"] == last_year, "Numeric"].values[0]

    sim_years, sim_values = simulate_annual_reduction(last_year, last_value, annual_reduction_rate, simulation_years)

    fig = px.line(df_malaria, x="YEAR (DISPLAY)", y="Numeric", title="Malaria Incidence with Simulation",
                  labels={"YEAR (DISPLAY)": "Year", "Numeric": "Malaria Incidence (per 1000 population)"},
                  markers=True)
    fig.add_scatter(x=sim_years, y=sim_values, mode="lines+markers",
                    name="Simulated Projection", line=dict(dash="dot", color="green"))
    fig.add_scatter(x=[target_year], y=[target_value], mode="markers+text",
                    name="Target",
                    marker=dict(symbol="star", size=12, color="red"),
                    text=[f"Target: {target_value}"], textposition="top center")

    st.plotly_chart(fig, use_container_width=True)
    st.markdown(f"**Simulation Summary:** With an annual reduction rate of {annual_reduction_rate:.1f}%, "
                f"malaria incidence is projected to be {sim_values[-1]:.1f} per 1000 population in {sim_years[-1]}.")


def run_example_simulation():
    """
    Example Streamlit app demonstrating projections and simulations.
    You can import and call this function in your main app or run standalone.
    """

    st.title("Strategic Health Projections & Simulations - Zambia")

    # Example dummy data for demonstration
    years = np.array([2016, 2017, 2018, 2019, 2020])
    values = np.array([350, 320, 300, 280, 260])

    df_example = pd.DataFrame({"Year": years, "Value": values})

    st.subheader("Example: Malaria Incidence Projection")
    fig1 = plot_trend_with_projection(df_example, "Year", "Value",
                                     title="Malaria Incidence Rate Projection",
                                     targets={2026: 201})
    st.plotly_chart(fig1)

    st.subheader("Example: Interactive Malaria Incidence Simulation")
    annual_reduction = st.slider("Annual Reduction Rate (%)", 0.0, 20.0, 5.0, 0.1)
    interactive_malaria_simulation(df_example.rename(columns={"Year": "YEAR (DISPLAY)", "Value": "Numeric"}),
                                  annual_reduction_rate=annual_reduction,
                                  simulation_years=5,
                                  target_year=2026,
                                  target_value=201)

