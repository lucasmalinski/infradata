import pandas as pd 
from pathlib import Path

def load_csv(f: Path, debug=False, encoding: str=None):
    candidates = [encoding] if encoding else ["utf-8", "cp1252", "latin-1"]
    for enc in candidates:
        try:
            df = pd.read_csv(f, encoding=enc, sep=None, engine="python")
            if debug:
                print(f"[csv_utils] Encoding used for {f.name}: {enc}")
            return df
        except UnicodeDecodeError:
            continue
    raise ValueError(f"[csv_utils] Could not decode {f}")