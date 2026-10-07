from pathlib import Path

import pandas as pd


# ============================================================
# 1. PARAMÈTRES
# ============================================================

ANNEE_DEBUT = 2022
ANNEE_FIN = 2025

BASE_DIR = Path(__file__).resolve().parents[2]

FICHIER_SIRENE = (
    BASE_DIR
    / "data"
    / "processed"
    / "table_analytique_restauration.csv"
)

FICHIER_TERRITOIRES = (
    BASE_DIR
    / "data"
    / "external"
    / "donnees_territoriales_insee.csv"
)

FICHIER_SORTIE = (
    BASE_DIR
    / "data"
    / "processed"
    / "dynamique_restauration_categorie.csv"
)


# ============================================================
# 2. CHARGEMENT
# ============================================================

df = pd.read_csv(
    FICHIER_SIRENE,
    sep=";",
    low_memory=False
)

territoires = pd.read_csv(
    FICHIER_TERRITOIRES,
    sep=";"
)


# ============================================================
# 3. NORMALISATION DES CODES COMMUNES
# ============================================================

df["code_commune"] = (
    df["code_commune"]
    .astype(str)
    .str.replace(".0", "", regex=False)
    .str.zfill(5)
)

territoires["code_commune"] = (
    territoires["code_commune"]
    .astype(str)
    .str.replace(".0", "", regex=False)
    .str.zfill(5)
)


# ============================================================
# 4. PRÉPARATION DES DATES
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
# 5. FILTRE SUR LA PÉRIODE
# ============================================================

debut = pd.Timestamp(f"{ANNEE_DEBUT}-01-01")
fin = pd.Timestamp(f"{ANNEE_FIN}-12-31")

creations = df[
    df["date_creation"].between(debut, fin)
].copy()

fermetures = df[
    df["date_fermeture"].between(debut, fin)
].copy()


# ============================================================
# 6. CRÉATIONS PAR COMMUNE ET CATÉGORIE
# ============================================================

creations_categories = (
    creations
    .groupby(
        ["code_commune", "categorie"]
    )
    .size()
    .unstack(fill_value=0)
    .reset_index()
)


# ============================================================
# 7. FERMETURES PAR COMMUNE ET CATÉGORIE
# ============================================================

fermetures_categories = (
    fermetures
    .groupby(
        ["code_commune", "categorie"]
    )
    .size()
    .unstack(fill_value=0)
    .reset_index()
)


# ============================================================
# 8. RENOMMAGE DES COLONNES
# ============================================================

categories = [
    "Restaurant",
    "Restauration rapide",
    "Café et bar"
]

for categorie in categories:

    if categorie not in creations_categories.columns:
        creations_categories[categorie] = 0

    if categorie not in fermetures_categories.columns:
        fermetures_categories[categorie] = 0


creations_categories = creations_categories.rename(
    columns={
        "Restaurant": "restaurants_creations",
        "Restauration rapide": "rapide_creations",
        "Café et bar": "cafes_bars_creations"
    }
)

fermetures_categories = fermetures_categories.rename(
    columns={
        "Restaurant": "restaurants_fermetures",
        "Restauration rapide": "rapide_fermetures",
        "Café et bar": "cafes_bars_fermetures"
    }
)


# ============================================================
# 9. TABLE DE BASE
# ============================================================

resultat = territoires[
    [
        "code_commune",
        "commune",
        "population_2023"
    ]
].copy()


# ============================================================
# 10. FUSION
# ============================================================

resultat = resultat.merge(
    creations_categories,
    on="code_commune",
    how="left"
)

resultat = resultat.merge(
    fermetures_categories,
    on="code_commune",
    how="left"
)


# ============================================================
# 11. REMPLACEMENT DES VALEURS MANQUANTES
# ============================================================

colonnes_flux = [
    "restaurants_creations",
    "rapide_creations",
    "cafes_bars_creations",
    "restaurants_fermetures",
    "rapide_fermetures",
    "cafes_bars_fermetures"
]

for colonne in colonnes_flux:

    resultat[colonne] = (
        resultat[colonne]
        .fillna(0)
        .astype(int)
    )


# ============================================================
# 12. CALCUL DES SOLDES PAR CATÉGORIE
# ============================================================

resultat["restaurants_solde"] = (
    resultat["restaurants_creations"]
    - resultat["restaurants_fermetures"]
)

resultat["rapide_solde"] = (
    resultat["rapide_creations"]
    - resultat["rapide_fermetures"]
)

resultat["cafes_bars_solde"] = (
    resultat["cafes_bars_creations"]
    - resultat["cafes_bars_fermetures"]
)


# ============================================================
# 13. TAUX RAPPORTÉS À LA POPULATION
# ============================================================

resultat["restaurants_solde_pour_1000"] = (
    resultat["restaurants_solde"]
    / resultat["population_2023"]
    * 1000
)

resultat["rapide_solde_pour_1000"] = (
    resultat["rapide_solde"]
    / resultat["population_2023"]
    * 1000
)

resultat["cafes_bars_solde_pour_1000"] = (
    resultat["cafes_bars_solde"]
    / resultat["population_2023"]
    * 1000
)


# ============================================================
# 14. SEGMENT DOMINANT DANS LA DYNAMIQUE
# ============================================================

def trouver_segment_dominant(row):

    soldes = {
        "Restaurant": row["restaurants_solde"],
        "Restauration rapide": row["rapide_solde"],
        "Café et bar": row["cafes_bars_solde"]
    }

    return max(
        soldes,
        key=soldes.get
    )


resultat["segment_dominant_dynamique"] = (
    resultat.apply(
        trouver_segment_dominant,
        axis=1
    )
)


# ============================================================
# 15. DYNAMIQUE TOTALE
# ============================================================

resultat["solde_total"] = (
    resultat["restaurants_solde"]
    + resultat["rapide_solde"]
    + resultat["cafes_bars_solde"]
)

resultat["solde_total_pour_1000"] = (
    resultat["solde_total"]
    / resultat["population_2023"]
    * 1000
)


# ============================================================
# 16. ARRONDIS
# ============================================================

colonnes_taux = [
    "restaurants_solde_pour_1000",
    "rapide_solde_pour_1000",
    "cafes_bars_solde_pour_1000",
    "solde_total_pour_1000"
]

resultat[colonnes_taux] = (
    resultat[colonnes_taux]
    .round(2)
)


# ============================================================
# 17. TRI
# ============================================================

resultat = resultat.sort_values(
    "solde_total_pour_1000",
    ascending=False
)


# ============================================================
# 18. EXPORT
# ============================================================

resultat.to_csv(
    FICHIER_SORTIE,
    sep=";",
    index=False
)


# ============================================================
# 19. CONTRÔLES
# ============================================================

print("=" * 70)
print("DYNAMIQUE DU MARCHÉ PAR CATÉGORIE")
print("=" * 70)

print(
    f"\nPériode étudiée : "
    f"{ANNEE_DEBUT}–{ANNEE_FIN}"
)

print("\nCréations par catégorie :")

print(
    f"Restaurants : "
    f"{resultat['restaurants_creations'].sum()}"
)

print(
    f"Restauration rapide : "
    f"{resultat['rapide_creations'].sum()}"
)

print(
    f"Cafés / bars : "
    f"{resultat['cafes_bars_creations'].sum()}"
)

print("\nFermetures par catégorie :")

print(
    f"Restaurants : "
    f"{resultat['restaurants_fermetures'].sum()}"
)

print(
    f"Restauration rapide : "
    f"{resultat['rapide_fermetures'].sum()}"
)

print(
    f"Cafés / bars : "
    f"{resultat['cafes_bars_fermetures'].sum()}"
)

print("\nSoldes par catégorie :")

print(
    f"Restaurants : "
    f"{resultat['restaurants_solde'].sum()}"
)

print(
    f"Restauration rapide : "
    f"{resultat['rapide_solde'].sum()}"
)

print(
    f"Cafés / bars : "
    f"{resultat['cafes_bars_solde'].sum()}"
)

print("\nSegment dominant par commune :")

print(
    resultat["segment_dominant_dynamique"]
    .value_counts()
    .to_string()
)

print("\nTop 10 des communes par dynamique totale :")

colonnes_affichage = [
    "commune",
    "restaurants_solde",
    "rapide_solde",
    "cafes_bars_solde",
    "solde_total",
    "solde_total_pour_1000",
    "segment_dominant_dynamique"
]

print(
    resultat[
        colonnes_affichage
    ]
    .head(10)
    .to_string(index=False)
)

print("\n" + "=" * 70)
print(f"Fichier créé : {FICHIER_SORTIE}")
print("=" * 70)