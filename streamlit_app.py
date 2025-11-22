
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from pathlib import Path

DATA_FILE = Path("/mnt/data/accident_dashboard_artifacts/clean_sample.csv")

@st.cache_data
def load_data():
    df = pd.read_csv(DATA_FILE)
    df['CRASH_DATETIME'] = pd.to_datetime(df.get('CRASH_DATETIME', df.columns[0]), errors='coerce')
    return df

def main():
    st.set_page_config(layout="wide", page_title="Accident Analytics Dashboard")
    st.markdown("<h1 style='text-align:center'>Accident Analytics & Risk Dashboard</h1>", unsafe_allow_html=True)

    df = load_data()
    st.sidebar.header("Filters")
    min_date = pd.to_datetime(df['CRASH_DATETIME']).min()
    max_date = pd.to_datetime(df['CRASH_DATETIME']).max()
    date_range = st.sidebar.date_input("Date range", [min_date.date(), max_date.date()])

    st.sidebar.markdown("## Scenario sliders")
    weather_factor = st.sidebar.slider("Weather severity multiplier", 0.5, 2.0, 1.0, 0.1)
    traffic_factor = st.sidebar.slider("Traffic density multiplier", 0.5, 2.0, 1.0, 0.1)
    visibility_factor = st.sidebar.slider("Visibility multiplier", 0.5, 2.0, 1.0, 0.1)

    st.sidebar.markdown("## Downloads")
    if st.sidebar.button("Download region risk CSV"):
        st.download_button("risk.csv", "region_risk_index.csv")

    # KPI row
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total incidents", int(len(df)))
    col2.metric("Avg incidents per day", round(len(df) / ( (pd.to_datetime(df['CRASH_DATETIME']).max() - pd.to_datetime(df['CRASH_DATETIME']).min()).days + 1), 2))
    col3.metric("Avg severity (score)", round(df['SEVERITY_SCORE'].mean(),2))
    col4.metric("Top region", df.get('BOROUGH', 'N/A').mode().iloc[0] if 'BOROUGH' in df.columns else "N/A")

    # Time series plot
    ts = df.groupby(pd.to_datetime(df['CRASH_DATETIME']).dt.date).size().rename('count').reset_index()
    ts['date'] = pd.to_datetime(ts['CRASH_DATETIME']) if 'CRASH_DATETIME' in ts.columns else pd.to_datetime(ts['date'])
    fig = px.line(ts, x='date', y='count', title='Incidents over time')
    st.plotly_chart(fig, use_container_width=True)

    # Map scatter (if lat/lon present)
    if 'LATITUDE' in df.columns and 'LONGITUDE' in df.columns:
        sample = df.dropna(subset=['LATITUDE','LONGITUDE']).head(10000)
        fig_map = px.scatter_mapbox(sample, lat='LATITUDE', lon='LONGITUDE', hover_data=['CRASH_DATETIME'], zoom=9, height=600)
        fig_map.update_layout(mapbox_style="open-street-map")
        st.plotly_chart(fig_map, use_container_width=True)

    st.markdown("## Hotspots (cluster centroids)")
    st.image("/mnt/data/accident_dashboard_artifacts/hotspots_centroids.png", use_column_width=True)

    st.markdown("## Severity distribution")
    st.image("/mnt/data/accident_dashboard_artifacts/severity_distribution.png", use_column_width=True)

if __name__ == '__main__':
    main()
