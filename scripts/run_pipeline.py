# %%
import os
from dotenv import load_dotenv

from infradata.utils.project_root import find_project_root
from infradata.utils.csv_utils import load_csv

# =======================================
# Concatenated ingestions imports
# =======================================
from infradata.ingestion.tipos_infracoes import ingest as ingest_tiposinfracoes
from infradata.ingestion.hist_infracoes import ingest as ingest_histinfracoes

# =======================================
# Transform imports
# ======================================= 
from infradata.transform.frota import transform as tf_frota 
from infradata.transform.acidentes import transform as tf_acidentes 
from infradata.transform.pedestres import transform as tf_mpedestres
from infradata.transform.indice import transform as tf_mortalidade
from infradata.transform.habilitados import transform as tf_habilitados 
from infradata.transform.tipos_infracoes import transform_all as tf_tiposinfracoes
from infradata.transform.hist_infracoes import transform as tf_histinfracoes




load_dotenv()

PROJECT_ROOT = find_project_root(__file__, debug= True)
RAW_DIR = PROJECT_ROOT / os.getenv("RAW_DATA_PATH")
SILVER_DIR = PROJECT_ROOT / os.getenv("SILVER_DATA_PATH")

# %%

# Filepaths
FROTA_PATH = RAW_DIR / "3.frota-de-veiculos-do-df-nos-ultimos-10-anos.csv"
ACFAT_PATH = RAW_DIR / "4.acidentes-de-transito-fatais-em-vias-urbanas-nos-ultimos-10-anos.csv"
PED_MORT_PATH = RAW_DIR / "5.pedestres-mortos-em-trechos-nao-semaforizados-nas-vias-do-distrito-federal-nos-ultimos-10-anos.csv"
INDICE_MORTOS_PATH = RAW_DIR /  "6.indice-mortos-por-10-mil-veiculos-no-df-nos-ultimos-10-anos.csv"
HABILITADOS_PATH = RAW_DIR / "11.numero-de-habilitados-no-distrito-federal-nos-ultimos-10-anos.csv"

# Directory paths
TIPOS_INFR_DIR = RAW_DIR / "tipos_infracao"
HIST_INFRACOES_DIR =  RAW_DIR / "historico_infracao"

def main():

    # Destination Filepaths defined by dict
    datasets = {
        'frota.csv' : tf_frota(load_csv(FROTA_PATH)),
        'acidentes.csv' : tf_acidentes(load_csv(ACFAT_PATH)),
        'mortes_pedestres_vias_nsem_sfaixa.csv' : tf_mpedestres(load_csv(PED_MORT_PATH)),
        'indice_mortos_por_10k_veiculos.csv' : tf_mortalidade(load_csv(INDICE_MORTOS_PATH)),
        'habilitados.csv' : tf_habilitados(load_csv(HABILITADOS_PATH)),
        
        # Directory Paths (Concatenados)
        'tipos_infracoes.csv' : tf_tiposinfracoes(ingest_tiposinfracoes(TIPOS_INFR_DIR)),
        'hist_infracoes.csv' : tf_histinfracoes(ingest_histinfracoes(HIST_INFRACOES_DIR))
    }

    for name, df in datasets.items():
        df.to_csv(SILVER_DIR / name)
        print(f"Saved file to {SILVER_DIR / name}")

   
if __name__ == "__main__":
    main()