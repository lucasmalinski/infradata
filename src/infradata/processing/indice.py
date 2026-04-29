import pandas as pd
from pathlib import Path
from infradata.utils.csv_utils import load_csv

# =======================================
# Tratamento 6.Indice de Mortos por 10k
# =======================================
def process(fpath: Path) -> pd.DataFrame:
    df = load_csv(fpath)
    df = df.set_index("ANO")
    return df