from src.utils.csv_utils import load_csv
from src.utils.transform_utils import MONTH_MAP
from pathlib import Path
import pandas as pd

# =======================================
# Tratamento 4.Acidentes Fatais
# =======================================

def process(fpath: Path) -> pd.DataFrame:
    acfat_via_urb = load_csv(fpath)

    acfat_via_urb = acfat_via_urb[acfat_via_urb['mes'] != 'Total']
    acfat_via_urb = acfat_via_urb.melt(
        id_vars="mes",
        var_name="ano",
        value_name="acidentes"
    )

    acfat_via_urb["ano"] = acfat_via_urb["ano"].astype(int)

    acfat_via_urb["mes_num"] = acfat_via_urb["mes"].map(MONTH_MAP)


    ordem_colunas = ['mes_num', 'mes', 'ano', 'acidentes']

    acfat_via_urb = acfat_via_urb[ordem_colunas]
    acfat_via_urb.columns = ['MES', 'MES_NOME', 'ANO', 'ACIDENTES']
    acfat_via_urb['DATA'] = (acfat_via_urb['MES'].astype(str).str.zfill(2)
                            + '/'
                            + acfat_via_urb['ANO'].astype(str)
                            )

    acfat_via_urb = acfat_via_urb.drop(columns=['MES', 'ANO'])

    acfat_via_urb = acfat_via_urb[['DATA', 'MES_NOME', 'ACIDENTES']]
    acfat_via_urb = acfat_via_urb.set_index(['DATA'])

    return acfat_via_urb