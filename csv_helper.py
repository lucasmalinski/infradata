from charset_normalizer import from_path
import pandas as pd 

def load_csv(f):
    f_encoding = from_path(f).best().encoding
    return pd.read_csv(f, encoding=f_encoding, sep=";")

cbox