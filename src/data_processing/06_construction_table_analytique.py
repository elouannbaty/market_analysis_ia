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
    / "sirene_restauration_enrichie.csv"
)

OUTPUT_FILE = (
    PROJECT_DIR
    / "data"
    / "processed"
    / "table_analytique_restauration.csv"
)


# ============================================================
# Paramètres
# ============================================================

DATE_REFERENCE = pd.Timestamp("2026-08-31")


# ============================================================
# Chargement
# ============================================================

print("Chargement de la base enrichie...")

df = pd.read_csv(
    DATA_FILE,
    sep=";"
)

print(f"Nombre d'établissements : {len(df):,}")


# ============================================================
# Conversion des dates
# ============================================================

df["date_creation"] = pd.to_datetime(
    df["date_creation"],
    errors="coerce"
)

df["date_fermeture"] = pd.to_datetime(
    df["date_fermeture"],
    errors="coerce"
)


# ============================================================
# Variables temporelles
# ============================================================

df["annee_creation"] = (
    df["date_creation"]
    .dt.year
)

df["annee_fermeture"] = (
    df["date_fermeture"]
    .dt.year
)


# ============================================================
# Durée d'activité
# ============================================================

df["date_fin_activite"] = (
    df["date_fermeture"]
    .fillna(DATE_REFERENCE)
)

df["duree_activite_ans"] = (
    (
        df["date_fin_activite"]
        - df["date_creation"]
    ).dt.days
    / 365.25
).round(1)


# ============================================================
# Indicateur d'établissement fermé
# ============================================================

df["est_ferme"] = (
    df["statut"] == "Fermé"
)


# ============================================================
# Sélection des variables analytiques
# ============================================================

columns_to_keep = [
    # Identité
    "siret",
    "siren",

    # Activité
    "code_naf",
    "categorie",
    "libelle",

    # Localisation
    "commune",
    "code_commune",
    "code_postal",
    "latitude",
    "longitude",

    # Statut et temporalité
    "statut",
    "est_ferme",
    "date_creation",
    "annee_creation",
    "date_fermeture",
    "annee_fermeture",
    "duree_activite_ans",

    # Caractéristiques
    "tranche_effectif",
    "employeur",
    "categorie_entreprise",
    "siege",

    # Identification commerciale
    "enseigne_1",
    "denomination",
]


df_analytique = df[columns_to_keep].copy()


# ============================================================
# Contrôles
# ============================================================

print("\nContrôles de la table analytique :")

print(
    f"Nombre de lignes : "
    f"{len(df_analytique):,}"
)

print(
    f"Nombre de colonnes : "
    f"{len(df_analytique.columns)}"
)

print(
    "\nDurées d'activité négatives :"
)

print(
    (
        df_analytique["duree_activite_ans"] < 0
    ).sum()
)

print(
    "\nAnnées de création :"
)

print(
    df_analytique["annee_creation"]
    .describe()
)

print(
    "\nRépartition actif / fermé :"
)

print(
    df_analytique["statut"]
    .value_counts()
)

print(
    "\nRépartition par catégorie :"
)

print(
    df_analytique["categorie"]
    .value_counts()
)


# ============================================================
# Export
# ============================================================

df_analytique.to_csv(
    OUTPUT_FILE,
    sep=";",
    index=False
)

print("\nTable analytique créée.")
print(f"Fichier : {OUTPUT_FILE}")