from src.utils.csv_utils import load_csv
from src.utils.df_utils import remove_thousands_separator
import pandas as pd

# =======================================
# Tratamento 3.Frota
# =======================================

def process(path: Path) -> pd.DataFrame:
    frota = load_csv(path) 
    frota = frota.set_index("ANO")
    frota = remove_thousands_separator(frota)
    frota = frota.astype(int)
    return frota