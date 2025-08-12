import streamlit as st
import plotly.express as px
from utils.data_loader import load_healthcare_access

st.title("🏥 Access to Health Care Analysis")

# Load data

df = load_healthcare_access()

st.subheader("Dataset Preview")
st.dataframe(df.head())

# Filter for Zambia only
zambia_df = df[df["CountryName"] == "Zambia"]

# Indicator frequency
st.subheader("Indicator Distribution")
indicator_counts = zambia_df["Indicator"].value_counts().reset_index()
indicator_counts.columns = ["Indicator", "Count"]

fig_indicators = px.bar(
    indicator_counts,
    x="Indicator",
    y="Count",
    title="Distribution of Health Care Indicators (Zambia)",
    labels={"Count": "Number of Records"},
)
st.plotly_chart(fig_indicators, use_container_width=True)

# Trend over time for selected indicator
st.subheader("Indicator Trend Over Time")
selected_indicator = st.selectbox(
    "Select an Indicator", zambia_df["Indicator"].unique()
)
indicator_df = zambia_df[zambia_df["Indicator"] == selected_indicator]

fig_trend = px.line(
    indicator_df,
    x="SurveyYear",
    y="Value",
    title=f"{selected_indicator} Over Time",
    markers=True
)
st.plotly_chart(fig_trend, use_container_width=True)
