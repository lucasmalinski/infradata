import os
import re
import pandas as pd    
from dotenv import load_dotenv
from infradata.utils.map_veiculos import VEHICLE_TYPE_MAPPING
from infradata.utils.project_root import find_project_root
from infradata.utils.map_siglas import sigla_map
from infradata.ingestion.hist_infracoes import ingest as ingest_histinfracoes


load_dotenv(dotenv_path="data_paths.env")

# Main Directory paths
PROJECT_ROOT = find_project_root(__file__, debug= True)
RAW_DIR = PROJECT_ROOT / os.getenv("RAW_DATA_PATH")
SILVER_DIR = PROJECT_ROOT / os.getenv("SILVER_DATA_PATH")
HIST_INFRACOES_DIR =  RAW_DIR / "historico_infracao"
NAME = 'hist_infracoes.csv'
CACHE = PROJECT_ROOT / "data" / "silver" / "hist_infracoes.csv"



def transform(df: pd.DataFrame, debug=False) -> pd.DataFrame:
    
    # =======================================
    # TIPO DE VEÍCULO
    # =======================================

    df["tipo_veiculo"] = (
            df["tipo_veiculo"]
            .str.upper()
            .str.strip()
        )

    df["tipo_veiculo"] = (
        df["tipo_veiculo"].map(VEHICLE_TYPE_MAPPING)
    )

    if debug:
        print(f"\nApplied veículos mapping to df[tipo_veiculo]: ")
        print(VEHICLE_TYPE_MAPPING)
    

    # =======================================
    # HORÁRIO DE COMETIMENTO 
    # =======================================

    # Junção da coluna data e hora, e conversão do resultado em datetime
    df["cometimento"] = df["cometimento"].astype(str) + " " + df["hora_cometimento"].astype(str)
    df["cometimento"] = pd.to_datetime(df["cometimento"], format="%d/%m/%Y %H:%M")

    # Criação de coluna numérica
    df["hora_cometimento"] = df["cometimento"].dt.hour
    # Implement hour and minute validation

    # =======================================
    # CÓDIGO DE INFRAÇÃO - DETALHAMENTO
    # =======================================

    # Identificando colunas em que a mesma descrição de infração é usada para mais de um código de infração
    problemas_de_codigo = (
        df.groupby("descricao")["tipo_infracao"]
        .nunique()
        .loc[lambda x: x > 1]
    )
    problemas_de_codigo

    # Ambiguidade checada vide tabela de códigos do RENAINF ("https://www.gov.br/transportes/pt-br/centrais-de-conteudo/tabela-codigo-infracoes-renainf-xlsx")
    mapping = {
        "5843-1": "Deixar de indicar c/ antec - início da marcha",
        "5843-2": "Deixar de indicar c/ antec - manobra de parar",
        "5843-3": "Deixar de indicar c/ antec - mudança de direção",
        "5843-4": "Deixar de indicar c/ antec - mudança de faixa",
    }
    df["descricao_corrigida"] = (
        df["tipo_infracao"].map(mapping)
        .fillna(df["descricao"])
    )

    

    # =======================================
    # LOCAL DE COMETIMENTO
    # =======================================
    if debug:
        print("\nExtraindo informações rodoviárias")

    KM_PAT = r'\bkm\s*(\d+[.,]\d+|\d+)\b'

    # Handles: SENTIDO, SENT., SENTINDO (typo), SENTIFI/SENTIFO (typos)
    # Stops before en-dash (–/\x96), a dash followed by uppercase, or end of string
    SENTIDO_PAT = (
        r'\b(senti(?:do|ndo|fi\w*|fo\w*)|sent\.?)\s*'
        r'([\w\s\/\-\.\,\(\)]+?)'
        r'(?=\s*[\x96\u2013]|\s*-\s*[A-Z]|\s*$)'
    )
    
    # Extracts: DF-025, DF 085, BR-040, DF001, etc. → normalized to DF-025
    ROAD_PAT = r'\b((?:DF|BR)\s*[-]?\s*\d{2,3})\b'
    SIGLA_PAT = r'\b(' + '|'.join(sigla_map.keys()) + r')\b'
    
    def extract_road_code(s):
        if pd.isna(s): return None
        s = str(s)
        m = re.search(SIGLA_PAT, s, re.IGNORECASE)
        if m:
            return sigla_map[m.group(1).upper()]
        m = re.search(ROAD_PAT, s, re.IGNORECASE)
        if not m: return None
        code = re.sub(r'[\s\-]+', '', m.group(1).upper())
        return re.sub(r'(DF|BR)(\d+)', r'\1-\2', code)

    def extract_km(s):
        if pd.isna(s): return None
        m = re.search(KM_PAT, s, re.IGNORECASE)
        return m.group(1).replace(',', '.') if m else None

    def extract_sentido(s):
        if pd.isna(s): return None
        m = re.search(SENTIDO_PAT, s, re.IGNORECASE)
        if not m: return None
        raw = (m.group(1) + ' ' + m.group(2)).strip()
        # Normalize typos
        raw = re.sub(r'\bsenti(?:ndo|fi\w*|fo\w*)\b', 'SENTIDO', raw, flags=re.IGNORECASE)
        raw = re.sub(r'\bsent\.?\b', 'SENT.', raw, flags=re.IGNORECASE)
        return raw.strip(' .,')  
    
    
    # TO-DO
    # =======================================
    # 1) Substituir string de infração por mapa de infrações vide código RENAINF
    # 2) Extrair KM de [auinf_local_rodovia]
    # 3) Extrair SENTIDO de [auinf_local_rodovia]
    # 4) Desafio: Interpretar rodovias como sentido e Sentidos cardeais como sentido para Crescente/Decrescente (geopandas)
            # Ideias:
            # Numeração de rodovias segue lógica, portanto ideal seria resolver cada rodovia isoladamente

                # Seria possível mapear lógica: [https://www.der.df.gov.br/documents/d/der/mapa_rodov_escala_1_170-000_2022-pdf]
                # 1) Por tipo
                # Faixa	Tipo	Lógica
                # DF-0xx	Radiais / contorno / Estradas-Parque	Ligadas ao centro de Brasília ou anel viário
                # DF-1xx	Longitudinais	Norte ↔ Sul
                # DF-2xx	Transversais	Leste ↔ Oeste
                # DF-3xx	Diagonais	Cortes diagonais
                # DF-4xx	Ligações	Conectam outras rodovias/localidades
                
                # Ex.: DF-001 Sentido DF-075
                    # Se o KM-0 coincide com a intersecção 
                        # Então estar rumo à intersecção == SENTIDO DECRESCENTE
                        # Desafio: "SENTIDO RODOVIÁRIA" quebra a lógica
                            # Reforço para resolver casos isolados... 
                            # DF-002 km 5.8 (eixão) sentido RODOVIÁRIA == SENTIDO DECRESCENTE pois o km_zero é na saída norte.

                # 2) Por Contexto 
                # Ex.: Km 0 da DF-075 é no RIACHO FUNDO, então DF-075 sentido Núcleo Bandeirante é necessariamente CRESCENTE

    # 5) Desafio: Interpretar Observações () distinguindo parênteses relativo a sentido dos relativos à pt. de referência.
    # 6) Desafio: Popular latitude e longitude
    #       # Ideias: 
    #       # Replicar lat/long de [rodovia+km+sentido] idênticos
    #       # Calcular lat/long geograficamente a partir de [rodovia+km+sentido] (TO-DO[4] é pré-requisito )
    # =======================================

    df['rodovia_codigo'] = df['auinf_local_rodovia'].apply(extract_road_code)

    # Only fill where target column is missing
    df['auinf_local_km'] = df['auinf_local_km'].fillna(
        df['auinf_local_rodovia'].apply(extract_km)
    )

    # Only fill where target column is missing
    df['auinf_local_referencia'] = df['auinf_local_referencia'].fillna(
        df['auinf_local_rodovia'].apply(extract_sentido)
    )
    
    return df

if __name__ == '__main__':
    
    df = transform(ingest_histinfracoes(HIST_INFRACOES_DIR, debug=True), debug=True)
    

    df.to_csv(SILVER_DIR / NAME)
    # =======================================
    # CSV saving expected from run_pipeline.py, uncomment for debugging purposes
    # =======================================