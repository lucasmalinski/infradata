
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