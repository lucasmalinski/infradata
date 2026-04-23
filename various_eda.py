# %%

from src.utils.csv_utils import load_csv
from pathlib import Path  
import pandas as pd

MAIN_DATA_DIR =  Path(__file__).resolve().parent / "raw_data"
FROTA_PATH = MAIN_DATA_DIR / "3.frota-de-veiculos-do-df-nos-ultimos-10-anos.csv"
ACFAT_PATH = MAIN_DATA_DIR / "4.acidentes-de-transito-fatais-em-vias-urbanas-nos-ultimos-10-anos.csv"
PED_MORT_NSEM_PATH = MAIN_DATA_DIR / "5.pedestres-mortos-em-trechos-nao-semaforizados-nas-vias-do-distrito-federal-nos-ultimos-10-anos.csv"
INDICE_MORTOS_PATH = MAIN_DATA_DIR /  "6.indice-mortos-por-10-mil-veiculos-no-df-nos-ultimos-10-anos.csv"
HABILITADOS_PATH = MAIN_DATA_DIR / "11.numero-de-habilitados-no-distrito-federal-nos-ultimos-10-anos.csv"

# %%

frota.to_csv("silver/frota.csv")
acfat_via_urb.to_csv("silver/acidentes_fatais_vias_urbanas.csv")
mortes_pedestres_nsem.to_csv("silver/mortes_pedestres_vias_nsem_sfaixa.csv")
mortos_por_10k.to_csv("silver/indice_mortos_por_10k_veiculos.csv")
habilitados.to_csv("silver/habilitados.csv")
# %%
