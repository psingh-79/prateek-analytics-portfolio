
# Accident Analytics Dashboard - Artifacts

Artifacts generated from the uploaded NYC collisions dataset.

**Contents** (saved in this folder):
- summary.json - quick dataset summary
- daily_counts.csv - aggregated daily counts
- forecast_30d.csv - 30-day forecast of incidents (Holt-Winters)
- hotspots.csv - DBSCAN hotspot clusters summary
- region_risk_index.csv - risk index per region (if region column exists)
- clean_sample.csv - sampled cleaned dataset for quick dashboard load (path: /mnt/data/accident_dashboard_artifacts/clean_sample.csv)
- images: daily_ts_forecast.png, top_causes.png, severity_distribution.png, hotspots_centroids.png
- streamlit_app.py - scaffold Streamlit app (single-file)
- requirements.txt - Python dependencies

## How to run locally
1. Create a virtualenv and install requirements from requirements.txt
2. Run: `streamlit run streamlit_app.py` from the OUT_DIR folder.
