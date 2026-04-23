def remove_thousands_separator(df: pd.DataFrame) -> pd.DataFrame:
    df = df.astype(str)
    return df.apply(lambda col: col.str.replace('.', '', regex=False)).astype(int)