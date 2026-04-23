# %%
from src.utils.csv_utils import load_csv
from mapping_veiculos import TIPO_VEICULO_MAP
from pathlib import Path  
import pandas as pd


HIST_INFRACOES_DIR =  Path(__file__).resolve().parent / "raw_data" / "historico_infracao"

# %%
historico_infracoes = pd.concat(
                    [
                        load_csv(f, debug=True).rename(columns=lambda c: c.strip().lower())
                        for f in HIST_INFRACOES_DIR.glob("*.csv")
                    ],
                    ignore_index=True
                    )

historico_infracoes["tipo_veiculo"] = (
    historico_infracoes["tipo_veiculo"]
    .str.upper()
    .str.strip()
)

historico_infracoes.replace("null", pd.NA, inplace=True)

historico_infracoes["cometimento"] = pd.to_datetime(
    historico_infracoes["cometimento"], dayfirst=True, errors="coerce"
)

# %%
historico_infracoes["tipo_veiculo"] = (
    historico_infracoes["tipo_veiculo"]
    .map(TIPO_VEICULO_MAP)
)
# %%
historico_infracoes.to_csv("silver/historico_infracoes.csv")
