from src.utils.csv_utils import load_csv
from src.utils.transform_utils import remove_thousands_separator
from pathlib import Path
import pandas as pd

# =======================================
# Tratamento 3.Frota
# =======================================

def process(fpath: Path) -> pd.DataFrame:
    df = load_csv(fpath) 
    df = df.set_index("ANO")
    df = remove_thousands_separator(df)
    df = df.astype(int)
    return df