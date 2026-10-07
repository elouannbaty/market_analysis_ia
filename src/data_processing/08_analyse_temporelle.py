from pathlib import Path

import pandas as pd


# ============================================================
# CONFIGURATION
# ============================================================

PROJECT_DIR = Path(__file__).resolve().parents[2]

DATA_FILE = (
    PROJECT_DIR
    / "data"
    / "processed"
    / "table_analytique_restauration.csv"
)

OUTPUT_FILE = (
    PROJECT_DIR
    / "data"
    / "processed"
    / "evolution_temporelle_restauration.csv"
)

ANNEE_DEBUT = 2008
ANNEE_FIN = 2025

# Le stock SIRENE utilisé pour notre étude correspond à août 2026.
DATE_REFERENCE = pd.Timestamp("2026-08-31")


# ============================================================
# 1. CHARGEMENT
# ============================================================

print("Chargement de la table analytique...")

df = pd.read_csv(DATA_FILE, sep=";")

print(f"Nombre d'établissements : {len(df):,}")


# ============================================================
# 2. PRÉPARATION DES DATES
# ============================================================

df["date_creation"] = pd.to_datetime(
    df["date_creation"],
    errors="coerce"
)

df["date_fermeture"] = pd.to_datetime(
    df["date_fermeture"],
    errors="coerce"
)

df["annee_creation"] = df["date_creation"].dt.year
df["annee_fermeture"] = df["date_fermeture"].dt.year


# ============================================================
# 3. CRÉATIONS PAR ANNÉE
# ============================================================

creations = (
    df
    .dropna(subset=["annee_creation"])
    .groupby("annee_creation")
    .size()
    .rename("creations")
)


# ============================================================
# 4. FERMETURES PAR ANNÉE
# ============================================================

fermetures = (
    df
    .dropna(subset=["annee_fermeture"])
    .groupby("annee_fermeture")
    .size()
    .rename("fermetures")
)


# ============================================================
# 5. TABLEAU TEMPOREL COMPLET
# ============================================================

annees = pd.Index(
    range(ANNEE_DEBUT, ANNEE_FIN + 1),
    name="annee"
)

evolution = pd.DataFrame(index=annees)

evolution["creations"] = (
    creations
    .reindex(annees)
    .fillna(0)
    .astype(int)
)

evolution["fermetures"] = (
    fermetures
    .reindex(annees)
    .fillna(0)
    .astype(int)
)

evolution["solde"] = (
    evolution["creations"]
    - evolution["fermetures"]
)


# ============================================================
# 6. STOCK ACTIF RECONSTITUÉ
# ============================================================

# Pour chaque année, on compte les établissements :
#
# - créés avant ou pendant l'année
# - et qui ne sont pas encore fermés à la fin de l'année.
#
# Cela permet d'obtenir une estimation du stock actif
# à la fin de chaque année.

stock_actif = []

for annee in annees:

    date_fin_annee = pd.Timestamp(
        f"{annee}-12-31"
    )

    nombre_actifs = (
        (
            df["date_creation"].notna()
        )
        & (
            df["date_creation"] <= date_fin_annee
        )
        & (
            df["date_fermeture"].isna()
            | (
                df["date_fermeture"] > date_fin_annee
            )
        )
    ).sum()

    stock_actif.append(nombre_actifs)

evolution["stock_actif"] = stock_actif


# ============================================================
# 7. ÉVOLUTION DU STOCK
# ============================================================

evolution["variation_stock"] = (
    evolution["stock_actif"]
    .diff()
    .fillna(0)
    .astype(int)
)


evolution["variation_stock_pct"] = (
    evolution["stock_actif"]
    .pct_change()
    * 100
).round(2)


# ============================================================
# 8. ANALYSE PAR CATÉGORIE
# ============================================================

categories = sorted(
    df["categorie"]
    .dropna()
    .unique()
)


# ------------------------------------------------------------
# Créations par catégorie
# ------------------------------------------------------------

creations_categories = pd.crosstab(
    df["annee_creation"],
    df["categorie"]
)

creations_categories = (
    creations_categories
    .reindex(annees, fill_value=0)
)


# ------------------------------------------------------------
# Fermetures par catégorie
# ------------------------------------------------------------

fermetures_categories = pd.crosstab(
    df["annee_fermeture"],
    df["categorie"]
)

fermetures_categories = (
    fermetures_categories
    .reindex(annees, fill_value=0)
)


# ------------------------------------------------------------
# Solde par catégorie
# ------------------------------------------------------------

solde_categories = (
    creations_categories
    - fermetures_categories
)


# ============================================================
# 9. AFFICHAGE PRINCIPAL
# ============================================================

print("\n" + "=" * 70)
print(
    f"ÉVOLUTION TEMPORELLE DU MARCHÉ "
    f"{ANNEE_DEBUT}-{ANNEE_FIN}"
)
print("=" * 70)

print("\nCréations, fermetures et solde :")

print(
    evolution[
        [
            "creations",
            "fermetures",
            "solde",
            "stock_actif",
            "variation_stock_pct",
        ]
    ]
)


# ============================================================
# 10. ANNÉES MARQUANTES
# ============================================================

annee_max_creation = evolution["creations"].idxmax()
maximum_creations = evolution["creations"].max()

annee_max_fermeture = evolution["fermetures"].idxmax()
maximum_fermetures = evolution["fermetures"].max()

annee_max_solde = evolution["solde"].idxmax()
maximum_solde = evolution["solde"].max()

annee_min_solde = evolution["solde"].idxmin()
minimum_solde = evolution["solde"].min()


print("\n" + "=" * 70)
print("POINTS MARQUANTS")
print("=" * 70)

print(
    f"\nPlus grand nombre de créations : "
    f"{annee_max_creation} "
    f"({maximum_creations:,})"
)

print(
    f"Plus grand nombre de fermetures : "
    f"{annee_max_fermeture} "
    f"({maximum_fermetures:,})"
)

print(
    f"Solde annuel maximal : "
    f"{annee_max_solde} "
    f"({maximum_solde:+,})"
)

print(
    f"Solde annuel minimal : "
    f"{annee_min_solde} "
    f"({minimum_solde:+,})"
)


# ============================================================
# 11. ÉVOLUTION PAR CATÉGORIE
# ============================================================

print("\n" + "=" * 70)
print("SOLDE PAR CATÉGORIE")
print("=" * 70)

print(solde_categories)


# ============================================================
# 12. 2026 : ANNÉE PARTIELLE
# ============================================================

creations_2026 = (
    df["annee_creation"] == 2026
).sum()

fermetures_2026 = (
    df["annee_fermeture"] == 2026
).sum()

solde_2026 = (
    creations_2026
    - fermetures_2026
)


print("\n" + "=" * 70)
print("2026 — ANNÉE PARTIELLE")
print("=" * 70)

print(
    f"\nDate de référence : "
    f"{DATE_REFERENCE.strftime('%d/%m/%Y')}"
)

print(
    f"Créations enregistrées : "
    f"{creations_2026:,}"
)

print(
    f"Fermetures enregistrées : "
    f"{fermetures_2026:,}"
)

print(
    f"Solde observé : "
    f"{solde_2026:+,}"
)

print(
    "\nAttention : 2026 n'est pas une année complète "
    "et ne doit pas être comparée directement aux années "
    "2008-2025."
)


# ============================================================
# 13. SAUVEGARDE
# ============================================================

evolution.to_csv(
    OUTPUT_FILE,
    sep=";"
)

print("\n" + "=" * 70)
print("SAUVEGARDE")
print("=" * 70)

print("\nAnalyse temporelle terminée.")
print(f"Fichier créé : {OUTPUT_FILE}")