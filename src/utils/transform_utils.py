import pandas as pd

# =======================================
# CONSTANT UTILS
# =======================================
MONTH_MAP = {
    'Janeiro':1, 'Fevereiro':2, 'Marco':3, 'Abril':4,
    'Maio':5, 'Junho': 6, 'Julho':7, 'Agosto':8,
    'Setembro':9, 'Outubro':10, 'Novembro':11, 'Dezembro':12
}


# =======================================
# FUNCTION UTILS
# =======================================
def remove_thousands_separator(df: pd.DataFrame) -> pd.DataFrame:
    df = df.astype(str)
    return df.apply(lambda col: col.str.replace('.', '', regex=False)).astype(int)

