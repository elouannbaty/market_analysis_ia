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
    / "analyse_geographique_restauration.csv"
)


# ============================================================
# 1. CHARGEMENT
# ============================================================

print("Chargement de la table analytique...")

df = pd.read_csv(DATA_FILE, sep=";")

print(f"Nombre d'établissements : {len(df):,}")


# ============================================================
# 2. VÉRIFICATION DES COMMUNES
# ============================================================

print("\nNombre de codes communes :")
print(df["code_commune"].nunique())

print("\nNombre de libellés de communes :")
print(df["commune"].nunique())


# ============================================================
# 3. ANALYSE PAR CODE COMMUNE
# ============================================================

analyse = (
    df
    .groupby("code_commune")
    .agg(
        commune=("commune", lambda x: x.mode().iloc[0]),
        etablissements_total=("siret", "count"),
        etablissements_actifs=("est_ferme", lambda x: (~x).sum()),
        etablissements_fermes=("est_ferme", "sum"),
        entreprises=("siren", "nunique"),
    )
)


# ============================================================
# 4. TAUX DE FERMETURE
# ============================================================

analyse["taux_fermeture"] = (
    analyse["etablissements_fermes"]
    / analyse["etablissements_total"]
    * 100
).round(2)


# ============================================================
# 5. RÉPARTITION PAR CATÉGORIE
# ============================================================

categories_communes = pd.crosstab(
    df["code_commune"],
    df["categorie"]
)

analyse = analyse.join(categories_communes)


# ============================================================
# 6. PART DE CHAQUE COMMUNE DANS LE MARCHÉ
# ============================================================

analyse["part_marche"] = (
    analyse["etablissements_total"]
    / analyse["etablissements_total"].sum()
    * 100
).round(2)


analyse["part_marche_actif"] = (
    analyse["etablissements_actifs"]
    / analyse["etablissements_actifs"].sum()
    * 100
).round(2)


# ============================================================
# 7. TRI
# ============================================================

analyse = analyse.sort_values(
    "etablissements_total",
    ascending=False
)


# ============================================================
# 8. AFFICHAGE GLOBAL
# ============================================================

print("\n" + "=" * 70)
print("MARCHÉ DE LA RESTAURATION PAR COMMUNE")
print("=" * 70)

print(
    analyse[
        [
            "commune",
            "etablissements_total",
            "etablissements_actifs",
            "etablissements_fermes",
            "entreprises",
            "taux_fermeture",
            "part_marche",
        ]
    ]
    .to_string()
)


# ============================================================
# 9. TOP 10 — NOMBRE TOTAL
# ============================================================

print("\n" + "=" * 70)
print("TOP 10 — NOMBRE TOTAL D'ÉTABLISSEMENTS")
print("=" * 70)

print(
    analyse[
        [
            "commune",
            "etablissements_total",
            "etablissements_actifs",
            "etablissements_fermes",
            "part_marche",
        ]
    ]
    .head(10)
    .to_string(index=False)
)


# ============================================================
# 10. TOP 10 — ÉTABLISSEMENTS ACTIFS
# ============================================================

print("\n" + "=" * 70)
print("TOP 10 — ÉTABLISSEMENTS ACTIFS")
print("=" * 70)

print(
    analyse
    .sort_values(
        "etablissements_actifs",
        ascending=False
    )
    [
        [
            "commune",
            "etablissements_actifs",
            "etablissements_total",
            "taux_fermeture",
        ]
    ]
    .head(10)
    .to_string(index=False)
)


# ============================================================
# 11. STRUCTURE PAR CATÉGORIE
# ============================================================

print("\n" + "=" * 70)
print("STRUCTURE PAR CATÉGORIE — TOP 10 COMMUNES")
print("=" * 70)

colonnes_categories = [
    "Restaurant",
    "Restauration rapide",
    "Café et bar",
]

colonnes_existantes = [
    colonne
    for colonne in colonnes_categories
    if colonne in analyse.columns
]

print(
    analyse[
        ["commune"] + colonnes_existantes
    ]
    .head(10)
    .to_string(index=False)
)


# ============================================================
# 12. TAUX DE FERMETURE
# ============================================================

print("\n" + "=" * 70)
print("TAUX DE FERMETURE")
print("=" * 70)

# On conserve uniquement les communes ayant au moins
# 20 établissements afin d'éviter les taux peu représentatifs.

communes_significatives = analyse[
    analyse["etablissements_total"] >= 20
]

print(
    communes_significatives
    .sort_values(
        "taux_fermeture",
        ascending=False
    )
    [
        [
            "commune",
            "etablissements_total",
            "etablissements_fermes",
            "etablissements_actifs",
            "taux_fermeture",
        ]
    ]
    .head(10)
    .to_string(index=False)
)


# ============================================================
# 13. CONTRÔLE FINAL
# ============================================================

print("\n" + "=" * 70)
print("CONTRÔLE FINAL")
print("=" * 70)

print(
    f"\nNombre de communes analysées : "
    f"{len(analyse)}"
)

print(
    f"Nombre total d'établissements : "
    f"{analyse['etablissements_total'].sum():,}"
)


# ============================================================
# 14. SAUVEGARDE
# ============================================================

analyse.to_csv(
    OUTPUT_FILE,
    sep=";"
)

print("\n" + "=" * 70)
print("SAUVEGARDE")
print("=" * 70)

print("\nAnalyse géographique terminée.")
print(f"Fichier créé : {OUTPUT_FILE}")