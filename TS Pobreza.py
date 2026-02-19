import pyreadstat
import pandas as pd
import numpy as np
import statsmodels.api as sm


# ─────────────────────────────────────────────
# 1. Ruta y lectura del archivo SPSS
# ─────────────────────────────────────────────

ruta = r"C:\Users\MARIELA-IICE\OneDrive - Universidad de Costa Rica\Mariela IICE\TS Pobreza\Enigh2018_CreaVar_ Personas_PUBLICA.sav"
#ruta = r"C:\Users\marie\OneDrive - Universidad de Costa Rica\Mariela IICE\TS Pobreza\Enigh2018_CreaVar_ Personas_PUBLICA.sav"




df, meta = pyreadstat.read_sav(
    ruta,
    apply_value_formats=False
)

print(f"Base cargada: {df.shape[0]} filas | {df.shape[1]} variables")

# ─────────────────────────────────────────────
# 2. Limpieza de valores perdidos (SPSS → NaN)
# ─────────────────────────────────────────────

if meta.missing_user_values:
    df = df.replace(meta.missing_user_values, np.nan)

# ─────────────────────────────────────────────
# 3. Diccionario de variables (tipo Variable View)
# ─────────────────────────────────────────────

vars_df = pd.DataFrame({
    "variable": df.columns,
    "label": meta.column_labels
})

print(df['ID_ZONA'].describe())



df['lp'] = df['ID_ZONA'].replace({1: 110456, 2: 84922})
df['lpe'] = df['ID_ZONA'].replace({1: 50311, 2: 41801})



# ─────────────────────────────────────────────
# 4. Guardar metadata relevante
# ─────────────────────────────────────────────

spss_meta = {
    "var_labels": meta.column_labels,
    "value_labels": meta.value_labels,
    "missing": meta.missing_user_values
}


# ─────────────────────────────────────────────
# 5. TSE
#SALUD
# ─────────────────────────────────────────────


print(df['P036_EBAIS'].describe())


print(df['P055_DIAS_INTERNAMIENTO'].describe())

# Copias de las variables P###
df['cons_EBAIS'] = df['P036_EBAIS']
df['cons_Clinica'] = df['P040_CLINICA']
df['cons_Hospital'] = df['P044_HOSPITAL']
df['dias_hosp'] = df['P055_DIAS_INTERNAMIENTO']


variables0 = ['cons_EBAIS', 'cons_Clinica', 'cons_Hospital', 'dias_hosp']


for col in variables0:
    # Si son NaN
    df[col] = df[col].fillna(0)
    # Si son texto 'missing'
    df[col] = df[col].replace('.', 0)



columnas_p = [
    'P048_MEDICAMENTOS',
    'P049_EXAMEN_LABORATORIO',
    'P050_EXAMEN_RADIOLOGICO',
    'P051_TRATAMIENTO_ESPECIAL',
    'P052_OTRO_EXAMEN'
]

columnas_destino = [
    'medicamentos',
    'laboratorio',
    'radiologico',
    'trat_especial',
    'otro_examen'
]

# 1. Inicializar columnas en 0 EN EL DATAFRAME
for col in columnas_destino:
    df[col] = 0

# 2. Copiar 1 solo cuando P == 1
for p_col, dest_col in zip(columnas_p, columnas_destino):
    df.loc[df[p_col] == 1, dest_col] = 1



df['tse_ss'] = (
    df['cons_EBAIS'] * 48691 +
    df['cons_Clinica'] * 50923.45 +
    df['cons_Hospital'] * 61798.43 +
    df['medicamentos'] * 2022.63 +
    df['laboratorio'] * 1292 +
    df['radiologico'] * 6696.99 +
    df['trat_especial'] * 8700 +
    df['otro_examen'] * 9305.43 +
    df['dias_hosp'] * 499324
)


cols = [
    'cons_EBAIS','cons_Clinica','cons_Hospital',
    'medicamentos','laboratorio','radiologico',
    'trat_especial','otro_examen','dias_hosp'
]

df[cols] = df[cols].fillna(0)

print(df['medicamentos'].describe())


print(df['tse_ss'].describe())


df['estudiante'] = (df['P010_CENTRO_EDUCATIVO'])



df.loc[df['estudiante'].isin([1, 2, 3, 4]), 'estudiante'] = 1


df['publico'] = (df['P010_CENTRO_EDUCATIVO'])


df.loc[df['publico'].isin([2, 3, 4]), 'publico'] = 0
df.loc[df['publico'].isin([1]), 'publico'] = 1



#Cinco niveles de educacion: preescolar basica, secundaria, tecnica y universitaria MMM
#Especial los pongo con escolar (asumo el mismo costo por estudiante) MMM
df['niveledu'] = (df['P007_ASISTE_EDUCACION'])


df.loc[df['niveledu'].isin([1,2]), 'niveledu'] = 1
df.loc[df['niveledu'].isin([7,3]), 'niveledu'] = 2
df.loc[df['niveledu'].isin([4]), 'niveledu'] = 3
df.loc[df['niveledu'].isin([5,8,9]), 'niveledu'] = 4
df.loc[df['niveledu'].isin([6]), 'niveledu'] = 5



print(df['niveledu'].describe())

df['niveledu_pub'] = (
    df['niveledu'] * df['publico']
    .fillna(0)
)



#2018: Costo mensual por estudiante  de los servicios de educación recibidos MMM
#Presscolar  c/ 70.372
#Primaria: c/  132.213
#Secundaria:  c/ 133.6756382
#Tecnica  c/ 210.749
#Terciaria: c/ 775.82

df['tse_e'] = (df['niveledu_pub']
        .replace({1:70372, 2:132213, 3:133675.6382, 4:210749, 5:775825, 0:0})
        .fillna(0)
               )

print(df.columns.tolist())

print(df['tse_e'].describe())




df['tse_e'] = (df['niveledu_pub']
        .replace({1:70372, 2:132213, 3:133675.6382, 4:210749, 5:775825, 0:0})
        .fillna(0)
               )

df['tse_e'] = (df['niveledu_pub']
        .replace({1:70372, 2:132213, 3:133675.6382, 4:210749, 5:775825, 0:0})
        .fillna(0)
               )


df['tse_e'] = (df['niveledu_pub']
        .replace({1:70372, 2:132213, 3:133675.6382, 4:210749, 5:775825, 0:0})
        .fillna(0)
               )




df['tse_paquetEscol'] = (df['P016_IMAS_IMPLEM_ESCOLAR']
        .replace({1:9091})
        .fillna(0)
               )

df['tse_becaTecnicos'] = (df['PS10_BECA_CURSOS_TECNICOS']
        .replace({1:186588,2:186588 })
        .fillna(0)
               )



df['tse_CentrosPAM'] = (df['PS15_DIAS_BENEFIC_ADULTOSMAY']
        .replace({1:27207*'PS15_DIAS_BENEFIC_ADULTOSMAY',7:27207*'PS15_DIAS_BENEFIC_ADULTOSMAY'})
        .fillna(0)
               )



df['tse_Alimentos_CEN'] = (df['PS16_RECIBE_ALIMENTOS_CEN']
        .replace({1:65722*'PS16_RECIBE_ALIMENTOS_CEN',3:65722*'PS16_RECIBE_ALIMENTOS_CEN'})
        .fillna(0)
               )


print(df['PS14_FRECUENCIA_DIAS_CUIDO'].describe())


df['tse_Cuido'] = (df['PS16_RECIBE_ALIMENTOS_CEN']
        .replace({1:123349*'PS14_FRECUENCIA_DIAS_CUIDO',3:65722*'PS16_RECIBE_ALIMENTOS_CEN'})
        .fillna(0)
               )



df["tse_cuido3H2"] = np.where(
    (df["P029_CUIDO"] == 3) & (df["PS13_HORARIO_SERV_CUIDO"] == 2),
    (123349 * df["PS14_FRECUENCIA_DIAS_CUIDO"]),
    np.nan
)

df["tse_cuido3H1"] = np.where(
    (df["P029_CUIDO"] == 3) & (df["PS13_HORARIO_SERV_CUIDO"] == 1) & (df["PS14_FRECUENCIA_DIAS_CUIDO"].between(1, 6)),
    (80177 * df["PS14_FRECUENCIA_DIAS_CUIDO"]) ,
    np.nan
)

df["tse_cuido1y2H2"] = np.where(
    ((df["P029_CUIDO"].isin([1, 2])) & (df["PS13_HORARIO_SERV_CUIDO"] == 2) & (df["PS14_FRECUENCIA_DIAS_CUIDO"].between(1, 6))),
    (158096 * df["PS14_FRECUENCIA_DIAS_CUIDO"]) ,
    np.nan
)

df["tse_cuido1y2H2"] = np.where(
    ((df["P029_CUIDO"].isin([1, 2])) & (df["PS13_HORARIO_SERV_CUIDO"] == 1) & (df["PS14_FRECUENCIA_DIAS_CUIDO"].between(1, 6))),
    (102762 * df["PS14_FRECUENCIA_DIAS_CUIDO"]) ,
    np.nan
)


df["tse_desay"] = np.where(
    df["P019_DESAYUNO_ESCOLAR"].between(1, 5),
    (df["P019_DESAYUNO_ESCOLAR"] * 27207),
    np.nan
)

df["tse_almuerA3"] = np.where(
    (df["P020_ALMUERZO_ESCOLAR"].between(1, 5)) & (df["P007_ASISTE_EDUCACION"] == 3),
    (df["P020_ALMUERZO_ESCOLAR"] * 37276),
    np.nan
)

df["tse_almuerA4"] = np.where(
    (df["P020_ALMUERZO_ESCOLAR"].between(1, 5)) & (df["P007_ASISTE_EDUCACION"] == 4),
    (df["P020_ALMUERZO_ESCOLAR"] * 45478),
    np.nan
)

df["tse_transp_e"] = np.where(
    df["P021_TRANSPORTE_ESCOLAR"].between(1, 5),
    (df["P021_TRANSPORTE_ESCOLAR"] * 64653),
    np.nan
)



ruta2 = r"C:\Users\MARIELA-IICE\OneDrive - Universidad de Costa Rica\Mariela IICE\TS Pobreza\Enigh2018_CreaVar_ Hogar_PUBLICA.sav"
#ruta2 = r"C:\Users\marie\OneDrive - Universidad de Costa Rica\Mariela IICE\TS Pobreza\Enigh2018_CreaVar_ Hogar_PUBLICA.sav"

df2, meta = pyreadstat.read_sav(
    ruta2,
    apply_value_formats=False
)

print(df2.shape)
print(df.shape)
df2["LLAVE_HOGAR"].duplicated().sum()


df_merge = df2.merge(
    df,
    on="LLAVE_HOGAR",
    how="left",
    validate="one_to_many"
)



print(df_merge.columns.tolist())


print(f"Base cargada: {df_merge.shape[0]} filas | {df_merge.shape[1]} variables")


df_merge["tse_bono"] = np.where(
    (df_merge["H090_BONO_VIVIENDA"] == 1) & (df_merge["ID_HOGAR_x"] == 1),
    (183013),
    np.nan
)


df_merge["tse_hconecq1"] = np.where(
    (df_merge["QUINTIL_NACIONAL_x"] == 1) & (df_merge["HG09_HOGARES_CONECTADOS"] == 1)&
    (df_merge["P001_PARENTESCO"] == 1),
    (12800),
    np.nan
)

df_merge["tse_hconecq2"] = np.where(
    (df_merge["QUINTIL_NACIONAL_x"] == 2) & (df_merge["HG09_HOGARES_CONECTADOS"] == 1) &
    (df_merge["P001_PARENTESCO"] == 1),
    (9600),
    np.nan
)

df_merge["tse_hconecq3"] = np.where(
    (df_merge["QUINTIL_NACIONAL_x"] == 3) & (df_merge["HG09_HOGARES_CONECTADOS"] == 1)&
    (df_merge["P001_PARENTESCO"] == 1),
    (6400),
    np.nan
)


df_merge['ID_ZONA_x'] = pd.to_numeric(df_merge['ID_ZONA_x'], errors='coerce')


lp_vals  = {1:110456, 2:84922}
lpe_vals = {1:50311, 2:41801}

df_merge['LP'] = (
    df_merge['ID_ZONA_x']
        .map(lp_vals)
        .astype(float)
)

df_merge['LPE'] = (
    df_merge['ID_ZONA_x']
        .map(lpe_vals)
        .astype(float)
)


df_merge[['LP', 'LPE']].describe()


# Lista de transferencias públicas
transfM_cols = [
    'P201_TRANSF_PENSION_IVMN_NET',
    'P203_TRANSF_PENSION_RNC',
    'P205_TRANF_BECA_SUP_TEC_PUB',
    'P207_TRANSF_BECA_PUBL_1Y2',
    'P208_TRANSF_AYUDA_PUB',
    'P216_INCAPACIDAD_ENFERMEDAD',
    'P217_LICENCIA_MATERNIDAD',
    'PS32_TRANSF_IMAS_NEGOCIO'
]



df_merge['TRANSFM_PUB_PC'] = (
    df_merge
        .groupby('LLAVE_HOGAR')[transfM_cols]
        .transform('sum')
        .sum(axis=1)
        .div(df_merge['H078_CANT_MIEMBROS_HOGAR'])
)



df_merge['APORTESS_PC'] = (
    df_merge
        .groupby('LLAVE_HOGAR')['P140_TOT_CONTRIB_SOCIALES']
        .transform('sum')
        /df_merge['H078_CANT_MIEMBROS_HOGAR']
)


print(df_merge['TRANSFM_PUB_PC'].describe())

# Lista de transferencias monetarias de la Seguridad social

df_merge['TOT_CONTRIB_SOCIALES_PAGADAS'] = (
    df_merge['P140_TOT_CONTRIB_SOCIALES'] * -1
)

transf_SS = [
    'P201_TRANSF_PENSION_IVMN_NET',
    'P217_LICENCIA_MATERNIDAD',
    'PS32_TRANSF_IMAS_NEGOCIO',
    'TOT_CONTRIB_SOCIALES_PAGADAS'
]


df_merge['TMSS_PC'] = (
    df_merge
        .groupby('LLAVE_HOGAR')[transf_SS]
        .transform('sum')
        .sum(axis=1)
        .div(df_merge['H078_CANT_MIEMBROS_HOGAR'])
)




df_merge['TESS_PC'] = (
    df_merge
        .groupby('LLAVE_HOGAR')['tse_ss']
        .transform('sum')
        / df_merge['H078_CANT_MIEMBROS_HOGAR']
)





# Transferencias públicas Monetarias
transf_M_Edu = [
    'P205_TRANF_BECA_SUP_TEC_PUB',
    'P207_TRANSF_BECA_PUBL_1Y2',
    'tse_becaTecnicos'
]


df_merge['TME_PC'] = (
    df_merge
        .groupby('LLAVE_HOGAR')[transf_M_Edu]
        .transform('sum')
        .sum(axis=1)
        .div( df_merge['H078_CANT_MIEMBROS_HOGAR'])
                         )


transf_E_Edu = [
    "tse_e",
    "tse_desay",
    "tse_almuerA3",
    "tse_almuerA4",
    "tse_transp_e"
]



df_merge['TEE_PC'] = (
    df_merge
        .groupby('LLAVE_HOGAR')[transf_E_Edu ]
        .transform('sum')
    .sum(axis=1)
    .div(df_merge['H078_CANT_MIEMBROS_HOGAR'])
)

transf_M_otras = [
    'P203_TRANSF_PENSION_RNC',
    'P208_TRANSF_AYUDA_PUB',
    'PS32_TRANSF_IMAS_NEGOCIO'
]




df_merge['TMO_PC'] = (
    df_merge
        .groupby('LLAVE_HOGAR')[transf_M_otras]
        .transform('sum')
        .sum(axis=1)
        .div(df_merge['H078_CANT_MIEMBROS_HOGAR'])
)

transf_E_otras= [
    'tse_paquetEscol',
    'tse_CentrosPAM',
    'tse_Alimentos_CEN',
    'tse_Cuido',
    'tse_cuido3H2',
    'tse_cuido3H1',
    'tse_cuido1y2H2',
    'tse_bono',
    'tse_hconecq1',
    'tse_hconecq2',
    'tse_hconecq3'
]

df_merge[transf_E_otras] = (
    df_merge[transf_E_otras]
        .apply(pd.to_numeric, errors='coerce')  # convierte texto a NaN
        .fillna(0)                              # reemplaza NaN por 0
)

df_merge['TEO_PC'] = (
    df_merge[transf_E_otras]
        .sum(axis=1)                              # suma por persona
        .groupby(df_merge['LLAVE_HOGAR'])
        .transform('sum')                         # suma por hogar
        .div(df_merge['H078_CANT_MIEMBROS_HOGAR'])
)


df_merge['TMTOT_PC'] = df_merge['TMSS_PC']+ df_merge['TME_PC']+ df_merge['TMO_PC']

df_merge['TETOT_PC'] = df_merge['TESS_PC']+ df_merge['TEE_PC']+ df_merge['TEO_PC']



# Pobreza
df_merge['POB'] = (df_merge['H192_ING_CORR_NETO_PC_SVL'] < df_merge['LP']).astype(int)

# Pobreza extrema
df_merge['POB_E'] = (df_merge['H192_ING_CORR_NETO_PC_SVL'] < df_merge['LPE']).astype(int)




# Ingreso neto sin transferencias
df_merge['Y_STS_SVL'] = df_merge['H192_ING_CORR_NETO_PC_SVL'] - df_merge['TRANSFM_PUB_PC']+df_merge['APORTESS_PC']

print(type(df_merge['Y_STS_SVL'].iloc[0]), type(df_merge['LP'].iloc[0]))

cols = ['Y_STS_SVL','LP','LPE']
df_merge[cols] = df_merge[cols].replace('.', 0)
df_merge[cols] = df_merge[cols].apply(pd.to_numeric, errors='coerce')


df_merge['Y_STS_SVL'] = pd.to_numeric(df_merge['Y_STS_SVL'], errors='coerce')


# Pobreza ST
df_merge['POB_STS'] = (df_merge['Y_STS_SVL'] < df_merge['LP']).astype(int)

# Pobreza extrema ST
df_merge['POB_E_STS'] = (df_merge['Y_STS_SVL'] < df_merge['LPE']).astype(int)






print(df_merge[["LP", "LPE"]].describe())
print(df_merge[['POB','POB_E', 'POB_STS','POB_E_STS']].describe())




print(df_merge['TMSS_PC'].describe())

df_merge['Y_TMSS_SVL'] = (df_merge['Y_STS_SVL']+ df_merge['TMSS_PC'])

# Pobreza TMSS
df_merge['POB_TMSS'] = (df_merge['Y_TMSS_SVL'] < df_merge['LP']).astype(int)

# Pobreza extrema TMSS
df_merge['POB_E_TMSS'] = (df_merge['Y_TMSS_SVL'] < df_merge['LPE']).astype(int)

print(df_merge[['POB_TMSS', 'POB_E_TMSS']].describe())




df_merge['Y_TESS_SVL'] = (df_merge['Y_STS_SVL']+ df_merge['TESS_PC'])

# Pobreza TESS
df_merge['POB_TESS'] = (df_merge['Y_TESS_SVL'] < df_merge['LP']).astype(int)


# Pobreza extrema TESS
df_merge['POB_E_TESS'] = (df_merge['Y_TESS_SVL'] < df_merge['LPE']).astype(int)

print(df_merge[['POB_TESS', 'POB_E_TESS']].describe())










pob_vars = df_merge.filter(regex='^POB').columns

for var in pob_vars:
    d = sm.stats.DescrStatsW(
        df_merge[var],
        weights=df_merge['FACTOR_y'],
        ddof=0
    )

    print(f"\nVariable: {var}")
    print("Tasa ponderada:", d.mean*100)
    print("Total ponderado:", d.sum)