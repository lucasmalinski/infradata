import pandas as pd 

def load_csv(f, debug=False, encoding=None):
    candidates = [encoding] if encoding else ["utf-8", "cp1252", "latin-1"]
    for enc in candidates:
        try:
            df = pd.read_csv(f, encoding=enc, sep=None, engine="python")
            if debug:
                print(f"Encoding used for {f.name}: {enc}")
            return df
        except UnicodeDecodeError:
            continue
    raise ValueError(f"Could not decode {f}")