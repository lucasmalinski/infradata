from infradata.utils.csv_utils import load_csv
from pathlib import Path

def ingest(dirpath: Path) -> dict:
    return {
        year: load_csv(dirpath / f"{year}.csv")
        for year in range (2018,2027)
    }