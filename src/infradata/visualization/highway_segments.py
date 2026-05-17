"""Carrega e renderiza geometrias de rodovias de GeoJSON como simples overlay."""

import json
from pathlib import Path
import geopandas as gpd


def load_highways_geojson(geojson_path: Path) -> gpd.GeoDataFrame:
    """
    Carrega geometrias de rodovias de GeoJSON (da API geo.py).
    Simples overlay - sem cálculos de densidade.
    
    Args:
        geojson_path: Caminho do arquivo GeoJSON (ex: data/external/rodovias_cache.geojson)
    
    Returns:
        GeoDataFrame com geometrias de rodovias
    """
    print("[highways] Carregando geometrias de rodovias do GeoJSON...")
    
    with open(geojson_path, "r", encoding="utf-8") as f:
        geojson_data = json.load(f)
    
    gdf = gpd.GeoDataFrame.from_features(geojson_data["features"], crs="EPSG:4326")
    
    print(f"[highways] Carregados {len(gdf)} segmentos de rodovia do GeoJSON")
    
    return gdf

