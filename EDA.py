# %%

from csv_helper import load_csv
from pathlib import Path  
import pandas as pd

MAIN_DATA_DIR =  Path(__file__).resolve().parent / "raw_data"
FROTA_PATH = MAIN_DATA_DIR / "3.frota-de-veiculos-do-df-nos-ultimos-10-anos.csv"
HABILITADOS_PATH = MAIN_DATA_DIR / "11.numero-de-habilitados-no-distrito-federal-nos-ultimos-10-anos.csv"
INDICE_MORTOS_PATH = MAIN_DATA_DIR /  "6.indice-mortos-por-10-mil-veiculos-no-df-nos-ultimos-10-anos.csv"


frota = load_csv(FROTA_PATH)
habilitados = load_csv(HABILITADOS_PATH)
mortos_por_10k = load_csv(INDICE_MORTOS_PATH)


# %%
# =======================================
# Tratamento Frota
# =======================================
frota = frota.set_index("ANO")
print(frota)


# %%
# =======================================
# Tratamento Habilitados
# =======================================
habilitados = habilitados.transpose()
habilitados.columns = ["total", "permissionario_pd", "condutor_definitivo_cnh"]
habilitados = habilitados.drop(index="Tipo")
habilitados.index.name = "ANO"
print(habilitados)

# %%
# =======================================
# Tratamento Indice de Mortos por 10k
# =======================================
mortos_por_10k = mortos_por_10k.set_index("ANO")


# %%

silver_frota = frota.to_csv("silver/frota.csv")
silver_habilitados = habilitados.to_csv("silver/habilitados.csv")
silver_indice = mortos_por_10k.to_csv("silver/indice.csv")
# %%
