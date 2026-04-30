from infradata.utils.csv_utils import load_csv
from infradata.utils.transform_utils import remove_thousands_separator
from pathlib import Path
import pandas as pd

# =======================================
# Tratamento 11.Habilitados
# =======================================

def transform(df: pd.DataFrame) -> pd.DataFrame:

    df = df.transpose()
    df.columns = ["total", "permissionario_pd", "condutor_definitivo_cnh"]
    df = df.drop(index="Tipo")
    df.index.name = "ANO"

    df = remove_thousands_separator(df)
    df = df.astype('int')
    return df