import streamlit as st
import geopandas as gpd
import plotly.express as px

st.title("🏥 Health Facilities Map")

try:
    gdf = gpd.read_file("data/zambia_health_facilities.geojson")

    # Create a column for hover info: prefer 'name', fallback to 'name:en', else 'Unknown'
    if 'name' in gdf.columns and gdf['name'].notnull().any():
        gdf['hover_name'] = gdf['name'].fillna(gdf.get('name:en', 'Unknown Facility'))
    elif 'name:en' in gdf.columns:
        gdf['hover_name'] = gdf['name:en'].fillna('Unknown Facility')
    else:
        gdf['hover_name'] = 'Unknown Facility'

    fig_map = px.scatter_mapbox(
        gdf,
        lat=gdf.geometry.y,
        lon=gdf.geometry.x,
        hover_name='hover_name',
        zoom=6,
        height=500,
        title="Health Facilities in Zambia"
    )
    fig_map.update_layout(
        mapbox_style="open-street-map",
        margin={"r":0, "t":40, "l":0, "b":0},
        hoverlabel=dict(bgcolor="white", font_size=12)
    )
    st.plotly_chart(fig_map, use_container_width=True)

except Exception as e:
    st.warning(f"Could not load map data: {e}")
