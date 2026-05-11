import os
import pandas as pd    
from dotenv import load_dotenv
from infradata.utils.map_veiculos import VEHICLE_TYPE_MAPPING
from infradata.utils.project_root import find_project_root
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
    
    df["tipo_veiculo"] = (
            df["tipo_veiculo"]
            .str.upper()
            .str.strip()
        )

    
    if debug:
        before_cometimento_null_rm = df["cometimento"].isna().sum()
        print(f"Number of nulls before null>NA replace and datetime conversion: {before_cometimento_null_rm}")

    df.replace("null", pd.NA, inplace=True)

    df["cometimento"] = pd.to_datetime(df["cometimento"], dayfirst=True, errors="coerce")

    if debug:
        after_cometimento_nareplace_dt_conversion =  df["cometimento"].isna().sum()
        print(f"Number of nulls after null>NA replace and datetime conversion: {after_cometimento_nareplace_dt_conversion}")

    df["tipo_veiculo"] = (
        df["tipo_veiculo"].map(VEHICLE_TYPE_MAPPING)
    )

    if debug:
        print(f"Applied veículos mapping to df[tipo_veiculo]: ")
        print(VEHICLE_TYPE_MAPPING)


    # Implement hour and minute validation

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
    
    #strings_hora_cometimento = df["hora_cometimento"].astype(str)
    #split = strings_hora_cometimento.str.split(":", expand=True)

    return df

if __name__ == '__main__':
    
    df = transform(ingest_histinfracoes(HIST_INFRACOES_DIR, debug=True), debug=True)
    
    # df.to_csv(SILVER_DIR / NAME)
    # =======================================
    # CSV saving expected from run_pipeline.py, uncomment for debugging purposes
    # =======================================

