"""Aplicativo Streamlit para visualização interativa de mapa geo de infrações."""

import streamlit as st
from pathlib import Path
import sys
import hashlib
from dotenv import load_dotenv

load_dotenv("data_paths.env")
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from infradata.visualization.build_map_cache import load_cache
from infradata.visualization.map_builder import build_base_map, add_clustered_points, add_heatmap_layer, add_highways_overlay
from infradata.visualization.filters import apply_all_filters, stats_sidebar
from infradata.visualization.highway_segments import load_highways_geojson
from infradata.utils.project_root import find_project_root
from streamlit_folium import st_folium

# ============================================================================
# CONFIGURAÇÃO DE PÁGINA
# ============================================================================
st.set_page_config(
    page_title="Infradata: Mapa de Infrações",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# TÍTULO E DESCRIÇÃO
# ============================================================================
st.title("🗺️ Mapa Interativo de Infrações de Trânsito - DF")
st.markdown("""
Visualização de infrações de trânsito no Distrito Federal com dados georreferenciados.
Explore a distribuição de infrações por rodovia, tipo de veículo e gravidade.

**Dados:** ~200k registros (2019-2023) com coordenadas geográficas | **API**: Geometrias de rodovias (GeoJSON)
""")

# ============================================================================
# CARREGA DADOS DO CACHE (reconstrói automaticamente se não existir)
# ============================================================================
@st.cache_data
def get_data():
    """Carrega dados de infrações em cache."""
    return load_cache()

@st.cache_data
def get_highways():
    """Carrega geometrias de rodovias do GeoJSON."""
    PROJECT_ROOT = find_project_root(__file__, debug=False)
    geojson_path = PROJECT_ROOT / "data" / "external" / "rodovias_cache.geojson"
    if geojson_path.exists():
        return load_highways_geojson(geojson_path)
    return None

with st.spinner("Carregando dados..."):
    df_full = get_data()
    gdf_highways = get_highways()

st.success(f"✅ Dados carregados: {len(df_full):,} infrações | {len(gdf_highways) if gdf_highways is not None else 0} rodovias")

# ============================================================================
# FILTROS DE BARRA LATERAL
# ============================================================================
st.sidebar.title("⚙️ Controles")
df_filtered = apply_all_filters(df_full)
stats_sidebar(df_filtered)

show_highways = st.sidebar.checkbox("Mostrar Rodovias (API GeoJSON)", value=True)

# ============================================================================
# EXIBIÇÃO DE MAPA COM OTIMIZAÇÃO DE PERFORMANCE
# ============================================================================
st.subheader(f"Mapa de Infrações ({len(df_filtered):,} pontos)")

# Performance: amostra grandes volumes com amostragem estratificada
max_points = 50000
if len(df_filtered) > max_points:
    st.info(f"⚡ Exibindo {max_points:,} amostra estratificada (de {len(df_filtered):,}) para performance")
    # Amostra estratificada por rodovia + gravidade para manter distribuição
    sample_frac = max_points / len(df_filtered)
    try:
        df_map = df_filtered.groupby(['rodovia_codigo', 'grav_tipo'], group_keys=False, observed=True).apply(
            lambda x: x.sample(frac=min(sample_frac, 1.0), random_state=42)
        ).head(max_points)
    except Exception:
        # Fallback para amostragem aleatória se estratificação falhar
        df_map = df_filtered.sample(n=max_points, random_state=42)
else:
    df_map = df_filtered

# Constrói mapa (Streamlit cacheia baseado nos dados)
@st.cache_data
def build_cached_map(df_data, include_highways=True, _highways_data=None):
    """Constrói e cacheia mapa baseado nos dados filtrados."""
    m = build_base_map()
    
    # Adiciona rodovias como simples overlay se disponível e requisitado
    if include_highways and _highways_data is not None and not _highways_data.empty:
        m = add_highways_overlay(m, _highways_data, show=True)
    
    m = add_clustered_points(
        m,
        df_data,
        color_by='grav_tipo',
        popup_cols=['rodovia_codigo', 'auinf_local_km', 'cometimento', 'grav_tipo', 'tipo_veiculo']
    )
    return m

m = build_cached_map(df_map, include_highways=show_highways, _highways_data=gdf_highways)

st_folium(m, width=1200, height=600)

# ============================================================================
# TABELA DE DADOS (OPCIONAL)
# ============================================================================
if st.checkbox("📊 Mostrar tabela de dados"):
    st.dataframe(
        df_filtered[['cometimento', 'rodovia_codigo', 'auinf_local_km', 'tipo_veiculo', 'grav_tipo', 'auinf_local_latitude', 'auinf_local_longitude']],
        use_container_width=True,
        height=400
    )

# ============================================================================
# RODAPÉ
# ============================================================================
st.markdown("---")
st.markdown("""
**Dados**: Histórico de Infrações - DF (2019-2023) | **API**: Rodovias GeoJSON | **Visualização**: Folium + Streamlit
""")
