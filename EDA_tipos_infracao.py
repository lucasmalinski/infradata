# %%
from csv_helper import load_csv
from pathlib import Path  
import pandas as pd

MAIN_DATA_DIR =  Path(__file__).resolve().parent / "raw_data"
TIPOS_INFR_DIR = MAIN_DATA_DIR / "tipos_infracao"


infracoes = {
    year: load_csv(TIPOS_INFR_DIR / f"{year}.csv")
    for year in range (2018,2027)
}
# %%
# =========================================
# Tratamento 10.Tipo de infrações cometidas
# =========================================

def treat_tipos_infracoes(df):     
    df = df.set_index('Tipo')
    df = df.T
    df = df.drop(index='Total')
    df = (df
                        .reset_index()
                        .rename(columns={'index': 'Mes'}))
    df.columns.name = None

    cols_to_treat = df.columns.drop('Mes')

    df = df.astype('str')
    df[cols_to_treat] = df[cols_to_treat].apply(
        lambda col:col.str.replace('.','',regex=False)
    )

    df[cols_to_treat] = df[cols_to_treat].apply(pd.to_numeric, errors='coerce')
    df.columns = df.columns.str.upper()

    month_map = {
        'JAN':1, 'FEV':2, 'MAR':3, 'ABR':4,
        'MAI':5, 'JUN':6, 'JUL':7, 'AGO':8,
        'SET':9, 'OUT':10, 'NOV':11, 'DEZ':12
        }

    df['MES'] = df['MES'].map(month_map)
    df = df.set_index('MES')
    return(df)

infracoes = {year: treat_tipos_infracoes(df) for year,df in infracoes.items()}

for year, df in infracoes.items():
    df.to_csv(f"silver/infracoes/infracoes_{year}.csv")

