# %%

from csv_helper import load_csv
from pathlib import Path  
import pandas as pd

MAIN_DATA_DIR =  Path(__file__).resolve().parent / "raw_data"
FROTA_PATH = MAIN_DATA_DIR / "3.frota-de-veiculos-do-df-nos-ultimos-10-anos.csv"
ACFAT_PATH = MAIN_DATA_DIR / "4.acidentes-de-transito-fatais-em-vias-urbanas-nos-ultimos-10-anos.csv"
PED_MORT_NSEM_PATH = MAIN_DATA_DIR / "5.pedestres-mortos-em-trechos-nao-semaforizados-nas-vias-do-distrito-federal-nos-ultimos-10-anos.csv"
INDICE_MORTOS_PATH = MAIN_DATA_DIR /  "6.indice-mortos-por-10-mil-veiculos-no-df-nos-ultimos-10-anos.csv"
HABILITADOS_PATH = MAIN_DATA_DIR / "11.numero-de-habilitados-no-distrito-federal-nos-ultimos-10-anos.csv"




# %%
# =======================================
# Tratamento 3.Frota
# =======================================
frota = load_csv(FROTA_PATH) 
frota = frota.set_index("ANO")
frota = frota.astype(str)

frota = frota.apply(
    lambda col: col.str.replace('.', '', regex=False)
    )

frota = frota.astype(int)
print(frota)

#%% 
# =======================================
# Tratamento 4.Acidentes Fatais
# =======================================
acfat_via_urb = load_csv(ACFAT_PATH)

acfat_via_urb = acfat_via_urb[acfat_via_urb['mes'] != 'Total']
acfat_via_urb = acfat_via_urb.melt(
    id_vars="mes",
    var_name="ano",
    value_name="acidentes"
)

acfat_via_urb["ano"] = acfat_via_urb["ano"].astype(int)

month_map = {'Janeiro':1, 'Fevereiro':2, 'Marco':3, 'Abril':4,
        'Maio':5, 'Junho': 6, 'Julho':7, 'Agosto':8,
        'Setembro':9, 'Outubro':10, 'Novembro':11, 'Dezembro':12}

acfat_via_urb["mes_num"] = acfat_via_urb["mes"].map(month_map)


ordem_colunas = ['mes_num', 'mes', 'ano', 'acidentes']

acfat_via_urb = acfat_via_urb[ordem_colunas]
acfat_via_urb.columns = ['MES', 'MES_NOME', 'ANO', 'ACIDENTES']
acfat_via_urb['DATA'] = (acfat_via_urb['MES'].astype(str).str.zfill(2)
                         + '/'
                         + acfat_via_urb['ANO'].astype(str)
                         )

acfat_via_urb = acfat_via_urb.drop(columns=['MES', 'ANO'])

acfat_via_urb = acfat_via_urb[['DATA', 'MES_NOME', 'ACIDENTES']]
acfat_via_urb = acfat_via_urb.set_index(['DATA'])


print(acfat_via_urb)

# %%
# =============================================
# Tratamento 5.Pedestres mortos 
# Trecos não semaforizados / sem faixa
# =============================================
mortes_pedestres_nsem = load_csv(PED_MORT_NSEM_PATH)

mortes_pedestres_nsem = mortes_pedestres_nsem.transpose()
mortes_pedestres_nsem = mortes_pedestres_nsem.rename(
    columns={0: 'pedestres_fatais'}
)
print(mortes_pedestres_nsem)

# %%
# =======================================
# Tratamento 6.Indice de Mortos por 10k
# =======================================
mortos_por_10k = load_csv(INDICE_MORTOS_PATH)

mortos_por_10k = mortos_por_10k.set_index("ANO")



# %%
# =======================================
# Tratamento 11.Habilitados
# =======================================
habilitados = load_csv(HABILITADOS_PATH)

habilitados = habilitados.transpose()
habilitados.columns = ["total", "permissionario_pd", "condutor_definitivo_cnh"]
habilitados = habilitados.drop(index="Tipo")
habilitados.index.name = "ANO"

habilitados = habilitados.astype('str')
habilitados = habilitados.apply(
    lambda col:col.str.replace('.','', regex=False)
)
habilitados = habilitados.astype('int')

print(habilitados)

# %%

silver_frota = frota.to_csv("silver/frota.csv")
silver_ac_fatais = acfat_via_urb.to_csv("silver/acidentes_fatais_vias_urbanas.csv")
silver_mortes_pedestres_vias_nsem_sfaixa = mortes_pedestres_nsem.to_csv("silver/mortes_pedestres_vias_nsem_sfaixa.csv")
silver_indice = mortos_por_10k.to_csv("silver/indice.csv")

silver_habilitados = habilitados.to_csv("silver/habilitados.csv")
# %%
