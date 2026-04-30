import geopandas as gpd
import requests
import json
from pathlib import Path

URL = "https://services7.arcgis.com/mLiYCaoVbEXk2abA/arcgis/rest/services/Rodovias_2025/FeatureServer/0/query?outFields=*&where=1%3D1&f=geojson"
CACHE_FILE = Path("rodovias_cache.geojson")

if CACHE_FILE.exists():
    print("Loading from cache...")
    with open(CACHE_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
else:
    print("Fetching from API (this may take a moment)...")
    r = requests.get(URL)
    r.raise_for_status() 
    data = r.json()

    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f)

df = gpd.GeoDataFrame.from_features(data["features"], crs="EPSG:4326")

# Final confirmation output
print("\n--- Execution Complete ---")
print(f"Rows: {len(df)}")
print(f"Columns: {list(df.columns)}")
print(df.head())