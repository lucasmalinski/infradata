# %%
from src.utils.csv_utils import load_csv
from src.utils.veiculos import VEHICLE_TYPE_MAPPING
from pathlib import Path  
import pandas as pd

def process(dirpath: Path) -> pd.DataFrame:

    df = pd.concat(
                        [
                            load_csv(f, debug=True).rename(columns=lambda c: c.strip().lower())
                            for f in dirpath.glob("*.csv")
                        ],
                        ignore_index=True
                        )

    df["tipo_veiculo"] = (
        df["tipo_veiculo"]
        .str.upper()
        .str.strip()
    )

    df.replace("null", pd.NA, inplace=True)

    df["cometimento"] = pd.to_datetime(df["cometimento"], dayfirst=True, errors="coerce")

    df["tipo_veiculo"] = (
        df["tipo_veiculo"].map(VEHICLE_TYPE_MAPPING)
    )
    return df


