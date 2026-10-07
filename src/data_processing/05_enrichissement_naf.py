from pathlib import Path

import pandas as pd


# ============================================================
# Chemins
# ============================================================

PROJECT_DIR = Path(__file__).resolve().parents[2]

DATA_FILE = (
    PROJECT_DIR
    / "data"
    / "processed"
    / "sirene_restauration.csv"
)

NAF_FILE = (
    PROJECT_DIR
    / "data"
    / "external"
    / "naf_restauration.csv"
)

OUTPUT_FILE = (
    PROJECT_DIR
    / "data"
    / "processed"
    / "sirene_restauration_enrichie.csv"
)


# ============================================================
# Chargement des données
# ============================================================

print("Chargement de la base SIRENE...")

df = pd.read_csv(
    DATA_FILE,
    sep=";"
)

print(f"Base SIRENE : {len(df):,} lignes")

print("\nChargement du référentiel NAF...")

naf = pd.read_csv(
    NAF_FILE,
    sep=";"
)

print(f"Référentiel NAF : {len(naf)} codes")


# ============================================================
# Contrôle du référentiel
# ============================================================

if naf["code_naf"].duplicated().any():
    raise ValueError(
        "Erreur : le référentiel contient des codes NAF en double."
    )


# ============================================================
# Jointure
# ============================================================

df = df.merge(
    naf,
    on="code_naf",
    how="left",
    validate="many_to_one"
)


# ============================================================
# Contrôle de la jointure
# ============================================================

codes_non_associes = df[
    df["categorie"].isna()
]["code_naf"].unique()

if len(codes_non_associes) > 0:
    raise ValueError(
        "Des codes NAF n'ont pas été associés : "
        f"{codes_non_associes}"
    )


# ============================================================
# Export
# ============================================================

df.to_csv(
    OUTPUT_FILE,
    sep=";",
    index=False
)


# ============================================================
# Résumé
# ============================================================

print("\nEnrichissement terminé.")
print(f"Fichier créé : {OUTPUT_FILE}")

print(f"\nNombre de lignes : {len(df):,}")
print(f"Nombre de colonnes : {len(df.columns)}")

print("\nRépartition par catégorie :")

print(
    df["categorie"]
    .value_counts()
)

print("\nRépartition par libellé :")

print(
    df["libelle"]
    .value_counts()
)