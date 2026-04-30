from infradata.utils.csv_utils import load_csv
from pathlib import Path
import pandas as pd


# =============================================
# Tratamento 5.Pedestres mortos 
# Trecos não semaforizados / sem faixa
# =============================================

def transform(df: pd.DataFrame) -> pd.DataFrame:

    df = df.transpose()
    df.columns = ['pedestres_fatais']
    df.index.name = 'ANO'
    
    return df

