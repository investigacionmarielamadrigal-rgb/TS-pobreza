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
