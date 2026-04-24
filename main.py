# %%
from src.processing.frota import process as process_frota 
from src.processing.acidentes import process as process_acidentes 
from src.processing.pedestres import process as process_mortes
from src.processing.indice import process as process_indice
from src.processing.habilitados import process as process_habilitados 
from src.processing.tipos_infracoes_eda import process as process_tipos_infracoes
from src.processing.hist_infracoes import process as process_hist_infracoes
from src.utils.dirpaths import RAW_DIR, SILVER_DIR


# Filepaths
FROTA_PATH = RAW_DIR / "3.frota-de-veiculos-do-df-nos-ultimos-10-anos.csv"
ACFAT_PATH = RAW_DIR / "4.acidentes-de-transito-fatais-em-vias-urbanas-nos-ultimos-10-anos.csv"
PED_MORT_PATH = RAW_DIR / "5.pedestres-mortos-em-trechos-nao-semaforizados-nas-vias-do-distrito-federal-nos-ultimos-10-anos.csv"
INDICE_MORTOS_PATH = RAW_DIR /  "6.indice-mortos-por-10-mil-veiculos-no-df-nos-ultimos-10-anos.csv"
HABILITADOS_PATH = RAW_DIR / "11.numero-de-habilitados-no-distrito-federal-nos-ultimos-10-anos.csv"

# Directory paths
TIPOS_INFR_DIR = RAW_DIR / "tipos_infracao"
HIST_INFRACOES_DIR =  RAW_DIR / "historico_infracao"

# %%

def main():

    # Isolated Files 
    datasets = {
        'frota.csv' : process_frota(FROTA_PATH),
        'acidentes.csv' : process_acidentes (ACFAT_PATH),
        'mortes_pedestres_vias_nsem_sfaixa.csv' : process_mortes(PED_MORT_PATH),
        'indice_mortos_por_10k_veiculos.csv' : process_indice(INDICE_MORTOS_PATH),
        'habilitados.csv' : process_habilitados(HABILITADOS_PATH),
        'tipos_infracoes.csv' : process_tipos_infracoes(TIPOS_INFR_DIR),
        'hist_infracoes.csv' : process_hist_infracoes(HIST_INFRACOES_DIR)
    }
    for name, df in datasets.items():
        df.to_csv(SILVER_DIR / name)

   
if __name__ == "__main__":
    main()