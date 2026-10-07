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

FICHIER_CONCENTRATION = (
    BASE_DIR
    / "data"
    / "processed"
    / "concentration_marche_restauration.csv"
)

FICHIER_SORTIE = (
    BASE_DIR
    / "data"
    / "processed"
    / "profils_marche_communes.csv"
)


# ============================================================
# 2. CHARGEMENT
# ============================================================

marche = pd.read_csv(
    FICHIER_MARCHE,
    sep=";",
    low_memory=False
)

dynamique = pd.read_csv(
    FICHIER_DYNAMIQUE,
    sep=";",
    low_memory=False
)

concentration = pd.read_csv(
    FICHIER_CONCENTRATION,
    sep=";",
    low_memory=False
)


# ============================================================
# 3. PRÉPARATION DE LA DYNAMIQUE
# ============================================================

dynamique = dynamique[
    [
        "commune",
        "creations_2022_2025",
        "fermetures_2022_2025",
        "solde_2022_2025",
    ]
].copy()

dynamique = dynamique.merge(
    marche[
        [
            "commune",
            "population_2023",
        ]
    ],
    on="commune",
    how="left"
)

dynamique["solde_pour_1000_hab"] = (
    dynamique["solde_2022_2025"]
    / dynamique["population_2023"]
    * 1000
)

dynamique = dynamique.drop(
    columns=["population_2023"]
)


# ============================================================
# 4. PRÉPARATION DE LA CONCENTRATION
# ============================================================

concentration = concentration[
    concentration["niveau"] == "commune"
].copy()

concentration = concentration[
    [
        "territoire",
        "etablissements_actifs",
        "entreprises_actives",
        "hhi",
        "cr5_pct",
        "cr10_pct",
    ]
].copy()

concentration = concentration.rename(
    columns={
        "territoire": "commune",
        "etablissements_actifs": "actifs_concentration",
        "entreprises_actives": "entreprises_concentration",
        "hhi": "hhi",
        "cr5_pct": "cr5_pct",
        "cr10_pct": "cr10_pct",
    }
)


# ============================================================
# 5. FUSION MARCHÉ + DYNAMIQUE
# ============================================================

profil = marche.merge(
    dynamique,
    on="commune",
    how="left"
)


# ============================================================
# 6. FUSION CONCENTRATION
# ============================================================

profil = profil.merge(
    concentration,
    on="commune",
    how="left"
)


# ============================================================
# 7. SÉLECTION DES VARIABLES
# ============================================================

colonnes = [
    "code_commune",
    "commune",
    "etablissements_total",
    "etablissements_actifs",
    "etablissements_fermes",
    "entreprises",
    "population_2023",
    "densite",
    "niveau_vie_median",
    "taux_fermeture",
    "etablissements_pour_1000_habitants",
    "actifs_pour_1000_habitants",
    "creations_2022_2025",
    "fermetures_2022_2025",
    "solde_2022_2025",
    "solde_pour_1000_hab",
    "hhi",
    "cr5_pct",
    "cr10_pct",
]

profil = profil[
    [
        colonne
        for colonne in colonnes
        if colonne in profil.columns
    ]
].copy()


# ============================================================
# 8. TRI
# ============================================================

profil = profil.sort_values(
    "etablissements_actifs",
    ascending=False
)


# ============================================================
# 9. AFFICHAGE
# ============================================================

print("=" * 70)
print("PROFILS DE MARCHÉ — NANTES MÉTROPOLE")
print("=" * 70)

print(
    f"\nCommunes analysées : {len(profil)}"
)

print(
    f"Colonnes produites : {len(profil.columns)}"
)


print("\nAperçu :")

colonnes_affichage = [
    "commune",
    "etablissements_actifs",
    "actifs_pour_1000_habitants",
    "solde_2022_2025",
    "solde_pour_1000_hab",
    "hhi",
    "cr5_pct",
]

print(
    profil[
        [
            colonne
            for colonne in colonnes_affichage
            if colonne in profil.columns
        ]
    ]
    .head(10)
    .to_string(index=False)
)


# ============================================================
# 10. CONTRÔLE DES DONNÉES MANQUANTES
# ============================================================

print("\n" + "=" * 70)
print("DONNÉES MANQUANTES")
print("=" * 70)

manquants = (
    profil
    .isna()
    .sum()
    .sort_values(
        ascending=False
    )
)

print(
    manquants[
        manquants > 0
    ]
    .to_string()
)

print("\n" + "=" * 70)
print("COMMUNES SANS DONNÉES DE DYNAMIQUE")
print("=" * 70)


# ============================================================
# 11. EXPORT
# ============================================================

profil.to_csv(
    FICHIER_SORTIE,
    sep=";",
    index=False
)


print("\n" + "=" * 70)
print(
    f"Fichier créé : {FICHIER_SORTIE}"
)
print("=" * 70)