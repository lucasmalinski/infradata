import json
import os
from pathlib import Path
import requests
from dotenv import load_dotenv
import geopandas as gpd
from infradata.utils.project_root import find_project_root

load_dotenv("data_paths.env")
PROJECT_ROOT = find_project_root(__file__, debug= True)



def ingest(URL: str, root: Path) -> gpd.GeoDataFrame:
    cache = Path(root / "data" / "external" / "rodovias_cache.geojson")
    if cache.exists():
        print("[geo.py] Loading from cache...")
        with open(cache, "r", encoding="utf-8") as f:
            data = json.load(f)
    else:
        print("[geo.py] Fetching from API (this may take a moment)...")
        r = requests.get(URL)
        r.raise_for_status() 
        data = r.json()

        with open(cache, "w", encoding="utf-8") as f:
            json.dump(data, f)

    gdf = gpd.GeoDataFrame.from_features(data["features"], crs="EPSG:4326")
    return gdf

if __name__ == "__main__":

    gdf = ingest(os.getenv("ROAD_DATA_URL"), root=PROJECT_ROOT)

