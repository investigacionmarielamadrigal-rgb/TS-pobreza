import pyreadstat
import pandas as pd
import numpy as np

# ─────────────────────────────────────────────
# 1. Ruta y lectura del archivo SPSS
# ─────────────────────────────────────────────

ruta = r"C:\Users\MARIELA-IICE\OneDrive - Universidad de Costa Rica\Mariela IICE\TS Pobreza\Enigh2018_CreaVar_ Personas_PUBLICA.sav"

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
# 4. Guardar metadata SPSS relevante
# ─────────────────────────────────────────────

spss_meta = {
    "var_labels": meta.column_labels,
    "value_labels": meta.value_labels,
    "missing": meta.missing_user_values
}

# ─────────────────────────────────────────────
# 5. Identificar factor de expansión
# ─────────────────────────────────────────────

candidatos_peso = [
    v for v in df.columns
    if any(k in v.lower() for k in ["expan", "peso", "factor", "pond"])
]

print("Posibles factores de expansión:")


for v in candidatos_peso:
    idx = df.columns.get_loc(v)
    print(f" - {v} → {meta.column_labels[idx]}")

# ─────────────────────────────────────────────
# 6. Definir peso (AJUSTAR al nombre correcto)
# ─────────────────────────────────────────────

factor = candidatos_peso[0]   # ← confirmar visualmente que es el correcto
df["weight"] = df[factor]

# Limpieza básica del peso
df = df[df["weight"] > 0]

print(df["weight"].describe())

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



df['tse_s'] = (
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


print(df['tse_s'].describe())


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



#(df['lp','lpe' ].describe())


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

gen temp5=(123349* PS14)/1000000  if ((P029_CUIDO==3 & PS13==2))




gen temp6=(80177* PS14)/1000000   if  ((P029_CUIDO==3 & PS13==1)& (PS14>= 1 & PS14 <= 6))
gen temp7=(158096* PS14)/1000000   if  (((P029_CUIDO==1|P029_CUIDO==2) & PS13==2)& (PS14>= 1 & PS14 <= 6))
gen temp8=(102762* PS14)/1000000  if  (((P029==1|P029_CUIDO==2) & PS13==1)& (PS14>= 1 & PS14 <= 6))
gen temp9= (P019*27207)/1000000 if (P019>= 1 & P019 <= 5)
gen temp10= (P020*37276)/1000000  if ((P020>= 1 & P020 <= 5) & P007==3)
gen temp11= (P020*45478)/1000000 if ((P020>= 1 & P020 <= 5)& P007==4)
gen temp12= (P021*64653)/1000000 if (P021>= 1 & P021<= 5)
gen temp13 = (183013/H078)/1000000 if H090==1 & hh==1
gen temp14= (12800*12)/1000000 if QUINTIL_NACIONAL==1 & HG09==1
gen temp15= (9600*12)/1000000 if QUINTIL_NACIONAL==2 & HG09==1
gen temp16= (6400*12)/1000000 if QUINTIL_NACIONAL==3 & HG09==1

egen tseot= rowtotal(temp1 temp2 temp3 temp4 temp5 temp6 temp7 temp8 temp9 temp10 temp11 temp12 temp13 temp14 temp15 temp16)
drop temp1 temp2 temp3 temp4 temp5 temp6 temp7 temp8 temp9 temp10 temp11 temp12 temp13 temp14 temp15 temp16
tab tseot [fw=FACTOR]


