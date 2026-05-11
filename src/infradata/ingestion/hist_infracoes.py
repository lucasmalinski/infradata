# %%
from infradata.utils.csv_utils import load_csv
from pathlib import Path  
import pandas as pd

# %% 
def ingest(dirpath: Path, debug: bool=False) -> pd.DataFrame:
    cache_raw_concat = dirpath / "cache.parquet"

    if cache_raw_concat.exists():
        if debug:
            print(f"[ingest/hist_infracoes.py] loading {cache_raw_concat}")
        df = pd.read_parquet(cache_raw_concat)

    else: 
        files = sorted(dirpath.glob("*.csv"))

        if not files:
            raise FileNotFoundError(f"Missing CSV raw files for {dirpath} ")
        
        if debug:
            print(f"[hist_infracoes.py] reading {len(files)} files")

        df = pd.concat(
                            [
                                load_csv(f, debug=True).rename(columns=lambda c: c.strip().lower())
                                for f in files
                            ],
                            ignore_index=True
                            )
        if debug:
            print(f"Concatenated {len(files)} files to shape: {df.shape}")

        df = df.astype("string")
        df.to_parquet(cache_raw_concat, index=False, engine="pyarrow")
    
        if debug: 
            print(f"[cache] saved at {cache_raw_concat}")


    return df