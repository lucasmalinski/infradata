import pandas as pd    
from infradata.utils.map_veiculos import VEHICLE_TYPE_MAPPING



def transform(df: pd.DataFrame, debug=False) -> pd.DataFrame:
    
    df["tipo_veiculo"] = (
            df["tipo_veiculo"]
            .str.upper()
            .str.strip()
        )

    
    if debug:
        before_cometimento_null_rm = df["cometimento"].isna().sum()
        print(f"Number of nulls before null>NA replace and datetime conversion: {before_cometimento_null_rm}")

    df.replace("null", pd.NA, inplace=True)

    df["cometimento"] = pd.to_datetime(df["cometimento"], dayfirst=True, errors="coerce")

    if debug:
        after_cometimento_nareplace_dt_conversion =  df["cometimento"].isna().sum()
        print(f"Number of nulls after null>NA replace and datetime conversion: {after_cometimento_nareplace_dt_conversion}")

    df["tipo_veiculo"] = (
        df["tipo_veiculo"].map(VEHICLE_TYPE_MAPPING)
    )

    if debug:
        print(f"Applied veículos mapping to df[tipo_veiculo]: ")
        print(VEHICLE_TYPE_MAPPING)


    # Implement hour and minute validation
    
    #strings_hora_cometimento = df["hora_cometimento"].astype(str)
    #split = strings_hora_cometimento.str.split(":", expand=True)

    return df

