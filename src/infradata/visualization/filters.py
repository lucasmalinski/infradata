"""Filtros de UI Streamlit para controles interativos do mapa."""

import streamlit as st
import pandas as pd


def sidebar_year_filter(df: pd.DataFrame, ano_col: str = 'ano') -> pd.DataFrame:
    """
    Slider de barra lateral para filtro de intervalo de anos.
    
    Args:
        df: DataFrame com coluna 'ano'
        ano_col: Nome da coluna de ano
    
    Returns:
        DataFrame filtrado
    """
    if ano_col not in df.columns:
        return df
    
    years = sorted(df[ano_col].dropna().unique())
    min_year, max_year = int(min(years)), int(max(years))
    
    st.sidebar.markdown("### Filtrar por Período")
    year_range = st.sidebar.slider(
        "Selecione o período (anos)",
        min_value=min_year,
        max_value=max_year,
        value=(min_year, max_year),
        step=1
    )
    
    df_filtered = df[(df[ano_col] >= year_range[0]) & (df[ano_col] <= year_range[1])]
    st.sidebar.info(f"📊 Registros selecionados: {len(df_filtered):,}")
    
    return df_filtered


def sidebar_rodovia_filter(df: pd.DataFrame, rodovia_col: str = 'rodovia_codigo') -> pd.DataFrame:
    """
    Multi-select de barra lateral para filtro de rodovia.
    
    Args:
        df: DataFrame com coluna rodovia
        rodovia_col: Nome da coluna código rodovia
    
    Returns:
        DataFrame filtrado
    """
    if rodovia_col not in df.columns:
        return df
    
    rodovias = sorted(df[rodovia_col].dropna().unique())
    
    if not rodovias:
        return df
    
    st.sidebar.markdown("### Filtrar por Rodovia")
    selected_roads = st.sidebar.multiselect(
        "Selecione rodovias (ou deixe em branco para todas):",
        options=rodovias,
        default=[]
    )
    
    if selected_roads:
        return df[df[rodovia_col].isin(selected_roads)]
    
    return df


def sidebar_severity_filter(df: pd.DataFrame, severity_col: str = 'grav_tipo') -> pd.DataFrame:
    """
    Multi-select de barra lateral para filtro de nível de gravidade.
    
    Args:
        df: DataFrame com coluna gravidade
        severity_col: Nome da coluna gravidade/severidade
    
    Returns:
        DataFrame filtrado
    """
    if severity_col not in df.columns:
        return df
    
    severities = sorted(df[severity_col].dropna().unique())
    
    if not severities:
        return df
    
    st.sidebar.markdown("### Filtrar por Gravidade")
    selected_severity = st.sidebar.multiselect(
        "Selecione nível de gravidade:",
        options=severities,
        default=severities  # All selected by default
    )
    
    if selected_severity:
        return df[df[severity_col].isin(selected_severity)]
    
    return df


def sidebar_vehicle_filter(df: pd.DataFrame, vehicle_col: str = 'tipo_veiculo') -> pd.DataFrame:
    """
    Multi-select de barra lateral para filtro de tipo de veículo.
    
    Args:
        df: DataFrame com coluna tipo veículo
        vehicle_col: Nome da coluna tipo veículo
    
    Returns:
        DataFrame filtrado
    """
    if vehicle_col not in df.columns:
        return df
    
    vehicles = sorted(df[vehicle_col].dropna().unique())
    
    if not vehicles:
        return df
    
    st.sidebar.markdown("### Filtrar por Tipo de Veículo")
    selected_vehicles = st.sidebar.multiselect(
        "Selecione tipos de veículo:",
        options=vehicles,
        default=[]
    )
    
    if selected_vehicles:
        return df[df[vehicle_col].isin(selected_vehicles)]
    
    return df


def apply_all_filters(df: pd.DataFrame) -> pd.DataFrame:
    """
    Aplica todos filtros de barra lateral em sequência.
    
    Args:
        df: DataFrame a filtrar
    
    Returns:
        DataFrame totalmente filtrado
    """
    df = sidebar_year_filter(df)
    df = sidebar_rodovia_filter(df)
    df = sidebar_severity_filter(df)
    df = sidebar_vehicle_filter(df)
    
    return df


def stats_sidebar(df: pd.DataFrame) -> None:
    """Exibe estatísticas na barra lateral."""
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📈 Estatísticas")
    
    col1, col2 = st.sidebar.columns(2)
    with col1:
        st.metric("Total", f"{len(df):,}")
    with col2:
        st.metric("Anos", f"{df['ano'].nunique() if 'ano' in df.columns else 'N/A'}")
    
    if 'grav_tipo' in df.columns:
        st.sidebar.markdown("**Por Gravidade:**")
        severity_counts = df['grav_tipo'].value_counts()
        for severity, count in severity_counts.items():
            st.sidebar.write(f"  • {severity}: {count:,}")
    
    if 'rodovia_codigo' in df.columns:
        st.sidebar.markdown("**Top 5 Rodovias:**")
        top_roads = df['rodovia_codigo'].value_counts().head(5)
        for road, count in top_roads.items():
            st.sidebar.write(f"  • {road}: {count:,}")
