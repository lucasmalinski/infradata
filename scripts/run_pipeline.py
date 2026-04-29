# %%
import os
from pathlib import Path
from infradata.processing.frota import process as process_frota 
from infradata.processing.acidentes import process as process_acidentes 
from infradata.processing.pedestres import process as process_mortes
from infradata.processing.indice import process as process_indice
from infradata.processing.habilitados import process as process_habilitados 
from infradata.processing.tipos_infracoes_eda import process as process_tipos_infracoes
from infradata.processing.hist_infracoes import process as process_hist_infracoes
from dotenv import load_dotenv

load_dotenv()

RAW_DIR = Path(os.getenv("RAW_DATA_PATH"))
SILVER_DIR = Path(os.getenv("SILVER_DATA_PATH"))

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

# %%

def main():

    # Isolated Files 
    datasets = {
        'frota.csv' : process_frota(FROTA_PATH),
        'acidentes.csv' : process_acidentes (ACFAT_PATH),
        'mortes_pedestres_vias_nsem_sfaixa.csv' : process_mortes(PED_MORT_PATH),
        'indice_mortos_por_10k_veiculos.csv' : process_indice(INDICE_MORTOS_PATH),
        'habilitados.csv' : process_habilitados(HABILITADOS_PATH),
        'tipos_infracoes.csv' : process_tipos_infracoes(TIPOS_INFR_DIR),
        'hist_infracoes.csv' : process_hist_infracoes(HIST_INFRACOES_DIR)
    }
    for name, df in datasets.items():
        df.to_csv(SILVER_DIR / name)
        print(f"Saved file to {SILVER_DIR / name}")

   
if __name__ == "__main__":
    main()