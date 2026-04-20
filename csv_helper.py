from charset_normalizer import from_path
import pandas as pd 

def load_csv(f, verbose=False):
    f_encoding = from_path(f).best().encoding
    if verbose:
        print (f"Encoding picked for csv: {f_encoding}")
    return pd.read_csv(f, encoding=f_encoding, sep=";")
    