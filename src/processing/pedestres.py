
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

