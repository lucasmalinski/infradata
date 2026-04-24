from src.utils.csv_utils import load_csv
from src.utils.transform_utils import remove_thousands_separator
from pathlib import Path
import pandas as pd


# =============================================
# Tratamento 5.Pedestres mortos 
# Trecos não semaforizados / sem faixa
# =============================================

def process(fpath: Path) -> pd.DataFrame:
    df = load_csv(fpath)

    df = df.transpose()
    df = df.rename(
        columns={0: 'pedestres_fatais'}
    )
    return df

