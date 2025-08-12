# utils/data_loader.py
import pandas as pd
import streamlit as st
import geopandas as gpd
import os

@st.cache_data
def load_data(path):
    if not os.path.exists(path):
        st.error(f"CSV file not found: {path}")
        st.stop()

    df = pd.read_csv(path)
    if 'Year' in df.columns:
        try:
            df['Year'] = pd.to_datetime(df['Year'], format='%Y', errors='coerce')
        except Exception as e:
            st.warning(f"Year column could not be parsed: {e}")
    return df

@st.cache_data
def load_geojson(path: str) -> gpd.GeoDataFrame:
    """Load a GeoJSON or zipped shapefile into a GeoDataFrame with validation."""
    if not os.path.exists(path):
        st.error(f"Geo file not found: {path}")
        st.stop()

    try:
        if path.endswith(".geojson"):
            gdf = gpd.read_file(path)
        elif path.endswith(".zip"):
            gdf = gpd.read_file(f"zip://{path}")
        else:
            st.error("Only .geojson or zipped shapefiles (.zip) are supported.")
            st.stop()

        if gdf is None or gdf.empty:
            st.error(f"Geo file loaded but contains no features: {path}")
            st.stop()

        if "geometry" not in gdf.columns:
            st.error("The file does not contain a 'geometry' column.")
            st.stop()

        return gdf

    except Exception as e:
        st.error(f"Failed to load geospatial data from {path}: {e}")
        st.stop()

@st.cache_data
def load_healthcare_access():
    path = "data/access-to-health-care.csv"
    if not os.path.exists(path):
        st.error(f"CSV file not found: {path}")
        st.stop()
    return pd.read_csv(path)

@st.cache_data
def load_covid_data():
    path = "data/covid-19-prevention_national_zmb.csv"
    if not os.path.exists(path):
        st.error(f"CSV file not found: {path}")
        st.stop()
    return pd.read_csv(path)

@st.cache_data
def load_dhs_data():
    path = "data/dhs-mobile_national_zmb.csv"
    if not os.path.exists(path):
        st.error(f"DHS CSV file not found: {path}")
        st.stop()
    return pd.read_csv(path)

@st.cache_data
def load_immunization():
    path = "data/immunization_national_zmb.csv"
    if not os.path.exists(path):
        st.error(f"CSV file not found: {path}")
        st.stop()
    return pd.read_csv(path)

@st.cache_data
def load_malaria():
    path = "data/malaria_indicators_zmb.csv"
    if not os.path.exists(path):
        st.error(f"CSV file not found: {path}")
        st.stop()
    return pd.read_csv(path, encoding="latin1")

@st.cache_data
def load_acute():
    path = "data/acute-respiratory-infection-ari_national_zmb.csv"
    if not os.path.exists(path):
        st.error(f"CSV file not found: {path}")
        st.stop()
    return pd.read_csv(path)

@st.cache_data
def load_health_insurance():
    path = "data/health-insurance_national_zmb.csv"
    if not os.path.exists(path):
        st.error(f"CSV file not found: {path}")
        st.stop()
    return pd.read_csv(path)

@st.cache_data
def load_sdgs():
    path = "data/sdgs_national_zmb.csv"
    if not os.path.exists(path):
        st.error(f"CSV file not found: {path}")
        st.stop()
    return pd.read_csv(path)

@st.cache_data
def load_tuberculosis():
    path = "data/tuberculosis_indicators_zmb.csv"
    if not os.path.exists(path):
        st.error(f"CSV file not found: {path}")
        st.stop()
    return pd.read_csv(path)

@st.cache_data
def load_hiv_prevalence():
    path = "data/hiv-prevalence_national_zmb.csv"
    if not os.path.exists(path):
        st.error(f"CSV file not found: {path}")
        st.stop()
    return pd.read_csv(path)
