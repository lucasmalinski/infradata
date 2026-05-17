"""Construir e cachear os dados geo filtrados para carregamento rápido da webapp."""

import os
import pickle
import pandas as pd
from pathlib import Path
from dotenv import load_dotenv

from infradata.utils.project_root import find_project_root

load_dotenv("data_paths.env")

PROJECT_ROOT = find_project_root(__file__, debug=False)
CACHE_DIR = PROJECT_ROOT / "data" / "vizcache"
CACHE_DIR.mkdir(parents=True, exist_ok=True)

DF_GEO_CACHE = CACHE_DIR / 'df_geo.pkl'


def _load_and_filter_geo_data() -> pd.DataFrame:
    """
    Carrega hist_infracoes.csv e filtra para linhas com coordenadas lat/lon válidas.
    
    Returns:
        DataFrame com ~200k linhas (lat/lon válidos, 2019-2025)
    """
    silver_dir = PROJECT_ROOT / os.getenv("SILVER_DATA_PATH", "data/silver")
    hist_path = silver_dir / "hist_infracoes.csv"
    
    if not hist_path.exists():
        raise FileNotFoundError(f"hist_infracoes.csv não encontrado em {hist_path}")
    
    print(f"[cache] Carregando {hist_path}...")
    df = pd.read_csv(hist_path, low_memory=False)
    
    lat_col = 'auinf_local_latitude'
    lon_col = 'auinf_local_longitude'
    
    if lat_col not in df.columns or lon_col not in df.columns:
        raise ValueError(f"Colunas esperadas {lat_col} e {lon_col} não encontradas")
    
    # Filtra linhas com lat e lon válidos (não NaN)
    df_geo = df[(df[lat_col].notna()) & (df[lon_col].notna())].copy()
    
    df_geo['cometimento'] = pd.to_datetime(df_geo['cometimento'], errors='coerce', dayfirst=True)
    df_geo['ano'] = df_geo['cometimento'].dt.year
    df_geo = df_geo[df_geo['ano'] < 2026]
    
    # Converte para numérico (valores inválidos se tornam NaN)
    df_geo[lat_col] = pd.to_numeric(df_geo[lat_col], errors='coerce')
    df_geo[lon_col] = pd.to_numeric(df_geo[lon_col], errors='coerce')
    
    # Remove NaN e coordenadas zero/inválidas (0,0 é inválido; Brasília é ~-15.8, -47.9)
    # Mantém limites razoáveis para DF: lat [-16.5 to -15.0], lon [-48.3 to -47.3]
    df_geo = df_geo[
        (df_geo[lat_col].notna()) & (df_geo[lon_col].notna()) &
        (df_geo[lat_col] != 0) & (df_geo[lon_col] != 0) &
        (df_geo[lat_col] >= -17) & (df_geo[lat_col] <= -15) &
        (df_geo[lon_col] >= -49) & (df_geo[lon_col] <= -47)
    ]
    
    print(f"[cache] Carregados {len(df_geo):,} registros com coordenadas válidas")
    
    return df_geo


def build_cache():
    """Constrói e cacheia dados geo. Chamado automaticamente se cache não existir."""
    if DF_GEO_CACHE.exists():
        print("[cache] ✅ Cache de dados geo existe")
        return
    
    print("[cache] Construindo cache de dados geo...")
    df_geo = _load_and_filter_geo_data()
    
    print(f"[cache] Salvando DataFrame ({len(df_geo):,} linhas) para {DF_GEO_CACHE}...")
    df_geo.to_pickle(DF_GEO_CACHE)
    print(f"[cache] ✅ Cache de dados geo pronto!")


def load_cache() -> pd.DataFrame:
    """
    Carrega dados geo cacheados. Constrói cache se não existir.
    
    Returns:
        df_geo: Dados de infrações filtrados com coordenadas válidas
    """
    build_cache()
    
    print("[cache] Carregando dados cacheados...")
    df_geo = pd.read_pickle(DF_GEO_CACHE)
    
    return df_geo


if __name__ == "__main__":
    build_cache()
