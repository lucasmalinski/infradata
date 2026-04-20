# %%

from csv_helper import load_csv
from pathlib import Path  

MAIN_DIR =  Path(__file__).resolve().parent
FROTA_PATH = MAIN_DIR / "raw_data" / "3.frota-de-veiculos-do-df-nos-ultimos-10-anos.csv"


frota = load_csv(FROTA_PATH)

frota

