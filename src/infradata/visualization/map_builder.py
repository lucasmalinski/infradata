"""Construtor de mapa Folium com clustering e features interativas."""

import folium
from folium.plugins import MarkerCluster, HeatMap, FastMarkerCluster
import pandas as pd
import numpy as np
import json


def build_base_map(center_lat: float = -15.8, center_lon: float = -47.9, zoom_start: int = 10) -> folium.Map:
    """
    Cria mapa base Folium centralizado em Brasília-DF com basemap em escala de cinza.
    
    Args:
        center_lat: Latitude do centro do mapa (padrão: Brasília)
        center_lon: Longitude do centro do mapa (padrão: Brasília)
        zoom_start: Nível de zoom inicial
    
    Returns:
        Objeto folium.Map
    """
    m = folium.Map(
        location=[center_lat, center_lon],
        zoom_start=zoom_start,
        tiles="CartoDB positron"
    )
    return m


def add_clustered_points(
    m: folium.Map,
    df: pd.DataFrame,
    lat_col: str = 'auinf_local_latitude',
    lon_col: str = 'auinf_local_longitude',
    color_by: str = 'grav_tipo',
    popup_cols: list = None
) -> folium.Map:
    """
    Adiciona marcadores clusterizados ao mapa com codificação de cores usando FastMarkerCluster.
    Otimizado para grandes volumes de dados (250k+ pontos).
    
    Args:
        m: Objeto folium.Map
        df: DataFrame com coordenadas
        lat_col: Nome da coluna latitude
        lon_col: Nome da coluna longitude
        color_by: Coluna para determinar cor do marcador (ex: 'grav_tipo' para gravidade)
        popup_cols: Colunas a exibir no popup ao clicar
    
    Returns:
        Mapa Folium atualizado
    """
    if popup_cols is None:
        popup_cols = ['rodovia_codigo', 'auinf_local_km', 'cometimento', 'grav_tipo']
    
    # Filtra apenas colunas disponíveis
    popup_cols = [c for c in popup_cols if c in df.columns]
    
    # Mapa de cores por gravidade
    color_map = {
        'Leve': 'blue',
        'Média': 'orange',
        'Grave': 'red',
        'Gravíssima': 'darkred',
        None: 'gray'
    }
    
    # Prepara dados para FastMarkerCluster (lat, lon, popup)
    points = []
    for idx, row in df.iterrows():
        lat = row[lat_col]
        lon = row[lon_col]
        
        if pd.isna(lat) or pd.isna(lon):
            continue
        
        # Constrói conteúdo do popup
        popup_text = "<br>".join([
            f"<b>{col}:</b> {row.get(col, 'N/A')}"
            for col in popup_cols
        ])
        
        color = color_map.get(row.get(color_by), 'gray')
        tooltip = f"{row.get('rodovia_codigo', 'Desconhecida')} - KM {row.get('auinf_local_km', '?')}"
        
        points.append([lat, lon, popup_text])
    
    if not points:
        return m
    
    # Usa FastMarkerCluster para performance com 200k+ pontos
    FastMarkerCluster(
        data=points,
        name="Infrações Clusterizadas"
    ).add_to(m)
    
    # Adiciona controle de camadas
    folium.LayerControl().add_to(m)
    
    return m


def add_heatmap_layer(
    m: folium.Map,
    df: pd.DataFrame,
    lat_col: str = 'auinf_local_latitude',
    lon_col: str = 'auinf_local_longitude',
    name: str = "Mapa de Calor de Densidade",
    show: bool = False
) -> folium.Map:
    """
    Adiciona camada de mapa de calor com escala de cor agressiva para melhor visibilidade.
    
    Args:
        m: Objeto folium.Map
        df: DataFrame com coordenadas (dados estratificados/amostrados)
        lat_col: Nome da coluna latitude
        lon_col: Nome da coluna longitude
        name: Nome da camada
        show: Se deve mostrar por padrão
    
    Returns:
        Mapa Folium atualizado
    """
    import numpy as np
    
    heat_data = []
    for idx, row in df.iterrows():
        if pd.notna(row[lat_col]) and pd.notna(row[lon_col]):
            heat_data.append([row[lat_col], row[lon_col]])
    
    if not heat_data:
        return m
    
    # Calcula intensidade para cada ponto baseado na densidade local de vizinhos
    lats = np.array([h[0] for h in heat_data])
    lons = np.array([h[1] for h in heat_data])
    
    # Encontra min/max de vizinhos para normalizar intensidade
    neighbor_counts = []
    for lat, lon in heat_data:
        neighbors = np.sum((np.abs(lats - lat) < 0.02) & (np.abs(lons - lon) < 0.02))
        neighbor_counts.append(neighbors)
    
    neighbor_counts = np.array(neighbor_counts)
    max_neighbors = np.max(neighbor_counts) if len(neighbor_counts) > 0 else 1
    
    # Cria dados ponderados com intensidade explícita [lat, lon, intensidade]
    heat_weighted = []
    for (lat, lon), count in zip(heat_data, neighbor_counts):
        # Normaliza intensidade para 0-1, com escala agressiva
        # Usa potência 1.5 para tornar diferenças mais visíveis
        intensity = (count / max_neighbors) ** 1.5
        heat_weighted.append([lat, lon, intensity])
    
    HeatMap(
        heat_weighted,
        name=name,
        radius=35,          # Raio maior para cobertura
        blur=50,            # Blur pesado para transições suaves
        max_zoom=16,
        min_opacity=0.05,   # Muito transparente em baixa densidade
        gradient={
            0.0: 'white',
            0.1: 'blue',
            0.2: 'cyan',
            0.35: 'lime',
            0.55: 'yellow',
            0.75: 'orange',
            1.0: 'red'
        },
        show=show
    ).add_to(m)
    
    return m


def add_highways_overlay(
    m: folium.Map,
    gdf_highways,
    color: str = '#555555',
    weight: int = 2,
    opacity: float = 0.6,
    name: str = "Rodovias (API GeoJSON)",
    show: bool = True
) -> folium.Map:
    """
    Add highway geometries as simple overlay on map (from GeoJSON API).
    
    Args:
        m: Folium Map object
        gdf_highways: GeoDataFrame with geometries from load_highways_geojson()
        color: Line color (hex)
        weight: Line width
        opacity: Line opacity (0-1)
        name: Layer name
        show: Whether to show by default
    
    Returns:
        Updated Folium Map
    """
    if gdf_highways is None or gdf_highways.empty:
        return m
    
    from shapely.geometry import LineString, MultiLineString
    
    # Create a feature group for highways
    highway_group = folium.FeatureGroup(name=name, show=show)
    
    for idx, highway in gdf_highways.iterrows():
        geometry = highway.geometry
        
        if geometry is None or geometry.is_empty:
            continue
        
        # Handle different geometry types
        if isinstance(geometry, MultiLineString):
            # Multi-part geometry: iterate through parts
            for geom_part in geometry.geoms:
                coords = [(lat, lon) for lon, lat in geom_part.coords]
                if coords:
                    road_name = highway.get('rodovia', 'Unknown')
                    folium.PolyLine(
                        locations=coords,
                        color=color,
                        weight=weight,
                        opacity=opacity,
                        tooltip=f"{road_name}"
                    ).add_to(highway_group)
        elif isinstance(geometry, LineString):
            # Single line: convert directly
            coords = [(lat, lon) for lon, lat in geometry.coords]
            if coords:
                road_name = highway.get('rodovia', 'Unknown')
                descricao = highway.get('descricao_inicial', '') + " → " + highway.get('descricao_final', '')
                popup_text = f"<b>{road_name}</b><br>{descricao}"
                
                folium.PolyLine(
                    locations=coords,
                    color=color,
                    weight=weight,
                    opacity=opacity,
                    popup=folium.Popup(popup_text, max_width=250),
                    tooltip=f"{road_name}"
                ).add_to(highway_group)
    
    highway_group.add_to(m)
    
    return m


def save_map(m: folium.Map, output_path: str) -> None:
    """Save map as HTML file."""
    m.save(output_path)
    print(f"[map_builder] Map saved to {output_path}")
