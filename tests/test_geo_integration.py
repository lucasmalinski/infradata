"""
Testes de integração para o consumo da API em geo.py.
Testa o fetch da API GeoJSON e o mecanismo de cache.
"""

import json
import os
import pytest
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock

from infradata.ingestion.geo import ingest
from infradata.utils.project_root import find_project_root


@pytest.fixture
def mock_geojson_response():
    """Resposta GeoJSON mockada da API."""
    return {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "properties": {"cod_rodovia": "DF001", "nome": "Estrada de Acesso Norte"},
                "geometry": {
                    "type": "LineString",
                    "coordinates": [[-47.8, -15.8], [-47.7, -15.7]]
                }
            },
            {
                "type": "Feature",
                "properties": {"cod_rodovia": "DF002", "nome": "Estrada de Acesso Sul"},
                "geometry": {
                    "type": "LineString",
                    "coordinates": [[-47.9, -15.9], [-47.8, -15.8]]
                }
            }
        ]
    }


@pytest.fixture
def temp_project_root():
    """Cria uma estrutura de projeto temporária para os testes."""
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir_path = Path(tmpdir)
        (tmpdir_path / "data" / "external").mkdir(parents=True, exist_ok=True)
        yield tmpdir_path


class TestGeoAPIIntegration:
    """Suíte de testes para a integração com a API GeoJSON."""

    def test_ingest_from_api_success(self, mock_geojson_response, temp_project_root):
        """Testa o fetch bem-sucedido da API e a criação do GeoDataFrame."""
        api_url = "https://example.com/api/roads"
        
        with patch("infradata.ingestion.geo.requests.get") as mock_get:
            mock_response = MagicMock()
            mock_response.json.return_value = mock_geojson_response
            mock_response.raise_for_status.return_value = None
            mock_get.return_value = mock_response
            
            gdf = ingest(api_url, root=temp_project_root)
            
            # Verifica se a API foi chamada
            mock_get.assert_called_once_with(api_url)
            
            # Verifica a estrutura do GeoDataFrame
            assert gdf is not None
            assert len(gdf) == 2
            assert gdf.crs.to_string() == "EPSG:4326"
            assert "geometry" in gdf.columns
            
            # Verifica se o arquivo de cache foi criado
            cache_path = temp_project_root / "data" / "external" / "rodovias_cache.geojson"
            assert cache_path.exists()
            
            # Verifica se o conteúdo do cache corresponde à resposta da API
            with open(cache_path, "r", encoding="utf-8") as f:
                cached_data = json.load(f)
            assert cached_data == mock_geojson_response

    def test_ingest_from_cache(self, mock_geojson_response, temp_project_root):
        """Testa o carregamento a partir do cache quando o arquivo já existe."""
        cache_path = temp_project_root / "data" / "external" / "rodovias_cache.geojson"
        
        # Pré-popula o cache
        with open(cache_path, "w", encoding="utf-8") as f:
            json.dump(mock_geojson_response, f)
        
        api_url = "https://example.com/api/roads"
        
        with patch("infradata.ingestion.geo.requests.get") as mock_get:
            # NÃO deve chamar a API se o cache existir
            gdf = ingest(api_url, root=temp_project_root)
            
            mock_get.assert_not_called()
            
            # Verifica se o GeoDataFrame ainda foi criado corretamente
            assert len(gdf) == 2
            assert gdf.crs.to_string() == "EPSG:4326"

    def test_ingest_api_failure(self, temp_project_root):
        """Testa o tratamento de falha na conexão com a API."""
        api_url = "https://example.com/api/roads"
        
        with patch("infradata.ingestion.geo.requests.get") as mock_get:
            mock_response = MagicMock()
            mock_response.raise_for_status.side_effect = Exception("HTTP 500")
            mock_get.return_value = mock_response
            
            with pytest.raises(Exception, match="HTTP 500"):
                ingest(api_url, root=temp_project_root)

    def test_ingest_response_structure(self, mock_geojson_response, temp_project_root):
        """Testa se a resposta da API possui a estrutura GeoJSON obrigatória."""
        api_url = "https://example.com/api/roads"
        
        with patch("infradata.ingestion.geo.requests.get") as mock_get:
            mock_response = MagicMock()
            mock_response.json.return_value = mock_geojson_response
            mock_response.raise_for_status.return_value = None
            mock_get.return_value = mock_response
            
            gdf = ingest(api_url, root=temp_project_root)
            
            # Verifica os tipos de geometria
            for idx, row in gdf.iterrows():
                assert row.geometry is not None
                assert row.geometry.geom_type in ["LineString", "MultiLineString", "Point"]

    def test_ingest_geojson_conversion(self, mock_geojson_response, temp_project_root):
        """Testa se as features GeoJSON são corretamente convertidas para GeoDataFrame."""
        api_url = "https://example.com/api/roads"
        
        with patch("infradata.ingestion.geo.requests.get") as mock_get:
            mock_response = MagicMock()
            mock_response.json.return_value = mock_geojson_response
            mock_response.raise_for_status.return_value = None
            mock_get.return_value = mock_response
            
            gdf = ingest(api_url, root=temp_project_root)
            
            # Verifica se as features estão acessíveis
            assert "cod_rodovia" in gdf.columns
            assert "nome" in gdf.columns
            assert gdf.loc[0, "cod_rodovia"] == "DF001"
            assert gdf.loc[1, "cod_rodovia"] == "DF002"