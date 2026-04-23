# %%
# =======================================
# Tratamento 6.Indice de Mortos por 10k
# =======================================
mortos_por_10k = load_csv(INDICE_MORTOS_PATH)

mortos_por_10k = mortos_por_10k.set_index("ANO")