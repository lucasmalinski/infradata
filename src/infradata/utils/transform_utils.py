import pandas as pd

# =======================================
# CONSTANT UTILS
# =======================================
LONG_MONTH_MAP = {
    'Janeiro':1, 'Fevereiro':2, 'Marco':3, 'Abril':4,
    'Maio':5, 'Junho': 6, 'Julho':7, 'Agosto':8,
    'Setembro':9, 'Outubro':10, 'Novembro':11, 'Dezembro':12
    }

MONTH_MAP = {
        'JAN':1, 'FEV':2, 'MAR':3, 'ABR':4,
        'MAI':5, 'JUN':6, 'JUL':7, 'AGO':8,
        'SET':9, 'OUT':10, 'NOV':11, 'DEZ':12
        }

# =======================================
# FUNCTION UTILS
# =======================================
def remove_thousands_separator(df: pd.DataFrame) -> pd.DataFrame:
    df = df.astype(str)
    return df.apply(lambda col: col.str.replace('.', '', regex=False)).astype(int)

