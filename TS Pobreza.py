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


vars_df   # display en PyCharm (Scientific Mode)

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


resultado = (
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


df['tses'] = (
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


print(df['tses'].describe())




gen student=P010_CENTRO_EDUCATIVO
recode student 1/4=1 .=0

gen public=P010
   recode public  2 3 4 9 =0

*Cinco niveles de educacion: preescolar basica, secundaria, tecnica y universitaria MMM
*Especial los pongo con escolar (asumo el mismo costo por estudiante) MMM
*en tecnica incluyo paraunivrsitaria, abierta (INA), especial y otra
gen levedu=P007
    recode levedu 1/2=1 7=2 3=2 4=3 5 8 9 =4 6=5 0=.
*replace levedu = 4 if levedu == 3 & inrange(P008_ULTIMO_GRADO, 31, 39)
tab P007 levedu,miss
tab levedu publ,miss

gen levedupub = levedu * publ /*se incluye solo los niveles de personas en público*/
recode levedupub .=0
lab def levedupu  1 "Preescolar" 2 "Primaria" 3 "Secundaria" 4 "Tecnica" 5"Superior" 0 "Ninguno"
lab val levedupu levedupu

tab levedupub,gen(epub)
ren epub2 edprespub
ren epub3 edprimpub
ren epub4 edsecpub
ren epub5 edtecpub
ren epub6 edsuppub
drop epub1

*2018: Costo mensual por estudiante  de los servicios de educación recibidos
*Basica: c/  117.606
*Media:  c/ 217.354
*Tecnica  c/ 210.749
*Terciaria: c/625.560


