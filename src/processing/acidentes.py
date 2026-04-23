
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