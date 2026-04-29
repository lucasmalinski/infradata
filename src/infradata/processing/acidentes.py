from infradata.utils.csv_utils import load_csv
from infradata.utils.transform_utils import LONG_MONTH_MAP
from pathlib import Path
import pandas as pd

# =======================================
# Tratamento 4.Acidentes Fatais
# =======================================

def process(fpath: Path) -> pd.DataFrame:
    df = load_csv(fpath)

    df = df[df['mes'] != 'Total']
    df = df.melt(
        id_vars="mes",
        var_name="ano",
        value_name="acidentes"
    )

    df["ano"] = df["ano"].astype(int)

    df["mes_num"] = df["mes"].map(LONG_MONTH_MAP)


    ordem_colunas = ['mes_num', 'mes', 'ano', 'acidentes']

    df = df[ordem_colunas]
    df.columns = ['MES', 'MES_NOME', 'ANO', 'ACIDENTES']
    df['DATA'] = (df['MES'].astype(str).str.zfill(2)
                            + '/'
                            + df['ANO'].astype(str)
                            )

    df = df.drop(columns=['MES', 'ANO'])

    df = df[['DATA', 'MES_NOME', 'ACIDENTES']]
    df = df.set_index(['DATA'])

    return df