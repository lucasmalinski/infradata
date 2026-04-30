from infradata.utils.csv_utils import load_csv
from infradata.utils.transform_utils import remove_thousands_separator
from pathlib import Path
import pandas as pd

# =======================================
# Tratamento 3.Frota
# =======================================

def transform(df: pd.DataFrame) -> pd.DataFrame:
    
    df = df.set_index("ANO")
    df = remove_thousands_separator(df)
    df = df.astype(int)
    return df