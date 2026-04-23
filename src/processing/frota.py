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