from pathlib import Path

import pandas as pd


# ============================================================
# 1. PARAMÈTRES
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[2]

FICHIER_MARCHE = (
    BASE_DIR
    / "data"
    / "processed"
    / "marche_restauration_territoire.csv"
)

FICHIER_DYNAMIQUE = (
    BASE_DIR
    / "data"
    / "processed"
    / "dynamique_restauration_commune.csv"
)

FICHIER_PROFILS = (
    BASE_DIR
    / "data"
    / "processed"
    / "profils_territoriaux.csv"
)

FICHIER_SORTIE = (
    BASE_DIR
    / "data"
    / "processed"
    / "analyse_opportunites_restauration.csv"
)


# ============================================================
# 2. CHARGEMENT
# ============================================================

marche = pd.read_csv(
    FICHIER_MARCHE,
    sep=";"
)

dynamique = pd.read_csv(
    FICHIER_DYNAMIQUE,
    sep=";"
)

profils = pd.read_csv(
    FICHIER_PROFILS,
    sep=";"
)


# ============================================================
# 3. NORMALISATION DES CODES COMMUNES
# ============================================================

for df in [marche, dynamique, profils]:

    df["code_commune"] = (
        df["code_commune"]
        .astype(str)
        .str.replace(".0", "", regex=False)
        .str.zfill(5)
    )


# ============================================================
# 4. SÉLECTION DES VARIABLES
# ============================================================

dynamique = dynamique[
    [
        "code_commune",
        "commune",
        "creations_2022_2025",
        "fermetures_2022_2025",
        "solde_2022_2025",
        "creations_pour_1000_habitants",
        "fermetures_pour_1000_habitants",
        "solde_pour_1000_habitants",
    ]
].copy()


profils = profils[
    [
        "code_commune",
        "territoire_dense",
        "intensite_offre",
        "profil_territorial",
        "ecart_offre_vs_mediane_pct",
    ]
].copy()


# ============================================================
# 5. FUSION
# ============================================================

analyse = marche.merge(
    dynamique,
    on="code_commune",
    how="left",
    suffixes=("", "_dynamique")
)

analyse = analyse.merge(
    profils,
    on="code_commune",
    how="left"
)


# ============================================================
# 6. MÉDIANES
# ============================================================

mediane_offre = (
    analyse["etablissements_pour_1000_habitants"]
    .median()
)

mediane_dynamique = (
    analyse["solde_pour_1000_habitants"]
    .median()
)


# ============================================================
# 7. CLASSIFICATION OFFRE / DYNAMIQUE
# ============================================================

analyse["offre_forte"] = (
    analyse["etablissements_pour_1000_habitants"]
    >= mediane_offre
)

analyse["dynamique_forte"] = (
    analyse["solde_pour_1000_habitants"]
    >= mediane_dynamique
)


def definir_typologie(row):

    if row["offre_forte"] and row["dynamique_forte"]:
        return "Offre forte / dynamique forte"

    elif row["offre_forte"] and not row["dynamique_forte"]:
        return "Offre forte / dynamique faible"

    elif not row["offre_forte"] and row["dynamique_forte"]:
        return "Offre faible / dynamique forte"

    else:
        return "Offre faible / dynamique faible"


analyse["typologie_marche"] = (
    analyse.apply(definir_typologie, axis=1)
)


# ============================================================
# 8. ÉCART À LA MÉDIANE
# ============================================================

analyse["ecart_dynamique_vs_mediane_pct"] = (
    (
        analyse["solde_pour_1000_habitants"]
        / mediane_dynamique
    ) - 1
) * 100


# ============================================================
# 9. PROFIL MARKET INTELLIGENCE
# ============================================================

analyse["profil_market_intelligence"] = "À surveiller"


analyse.loc[
    (
        ~analyse["offre_forte"]
        & analyse["dynamique_forte"]
    ),
    "profil_market_intelligence"
] = "Signal intéressant"


analyse.loc[
    (
        analyse["offre_forte"]
        & analyse["dynamique_forte"]
    ),
    "profil_market_intelligence"
] = "Marché dynamique"


analyse.loc[
    (
        analyse["offre_forte"]
        & ~analyse["dynamique_forte"]
    ),
    "profil_market_intelligence"
] = "Marché établi"


# ============================================================
# 10. ARRONDIS
# ============================================================

analyse["ecart_dynamique_vs_mediane_pct"] = (
    analyse["ecart_dynamique_vs_mediane_pct"]
    .round(2)
)


# ============================================================
# 11. EXPORT
# ============================================================

analyse.to_csv(
    FICHIER_SORTIE,
    sep=";",
    index=False
)


# ============================================================
# 12. CONTRÔLES
# ============================================================

print("=" * 70)
print("ANALYSE MARKET INTELLIGENCE")
print("=" * 70)

print(
    f"\nMédiane offre : "
    f"{mediane_offre:.2f} établissements / 1 000 habitants"
)

print(
    f"Médiane dynamique : "
    f"{mediane_dynamique:.2f} établissements / 1 000 habitants"
)

print("\nRépartition des typologies :")

print(
    analyse["typologie_marche"]
    .value_counts()
    .to_string()
)

print("\nCommunes avec un signal intéressant :")

colonnes_affichage = [
    "commune",
    "etablissements_pour_1000_habitants",
    "solde_2022_2025",
    "solde_pour_1000_habitants",
    "population_2023",
    "densite_2023",
    "niveau_vie_median",
    "typologie_marche",
]

print(
    analyse[
        analyse["profil_market_intelligence"]
        == "Signal intéressant"
    ][colonnes_affichage]
    .sort_values(
        "solde_pour_1000_habitants",
        ascending=False
    )
    .to_string(index=False)
)

print("\n" + "=" * 70)
print(f"Fichier créé : {FICHIER_SORTIE}")
print("=" * 70)