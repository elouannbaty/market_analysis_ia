from pathlib import Path

import pandas as pd


# ============================================================
# 1. PARAMÈTRES
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[2]

FICHIER_ENTREE = (
    BASE_DIR
    / "data"
    / "processed"
    / "profils_marche_communes.csv"
)

FICHIER_SORTIE = (
    BASE_DIR
    / "data"
    / "processed"
    / "profils_qualitatifs_communes.csv"
)


# ============================================================
# 2. CHARGEMENT
# ============================================================

df = pd.read_csv(
    FICHIER_ENTREE,
    sep=";",
    low_memory=False
)


# ============================================================
# 3. SEUILS
# ============================================================

mediane_offre = df["actifs_pour_1000_habitants"].median()

mediane_dynamique = df["solde_pour_1000_hab"].median()

mediane_cr5 = df["cr5_pct"].median()


print("=" * 70)
print("SEUILS DE CLASSIFICATION")
print("=" * 70)

print(
    f"Médiane offre : {mediane_offre:.2f} établissements / 1 000 habitants"
)

print(
    f"Médiane dynamique : {mediane_dynamique:.2f} établissement / 1 000 habitants"
)

print(
    f"Médiane CR5 : {mediane_cr5:.2f} %"
)


# ============================================================
# 4. NIVEAU D'OFFRE
# ============================================================

df["niveau_offre"] = pd.NA

df.loc[
    df["actifs_pour_1000_habitants"] >= mediane_offre,
    "niveau_offre"
] = "Forte"

df.loc[
    df["actifs_pour_1000_habitants"] < mediane_offre,
    "niveau_offre"
] = "Faible"


# ============================================================
# 5. DYNAMIQUE DU MARCHÉ
# ============================================================

df["dynamique_marche"] = pd.NA

df.loc[
    df["solde_pour_1000_hab"] >= mediane_dynamique,
    "dynamique_marche"
] = "Forte"

df.loc[
    df["solde_pour_1000_hab"] < mediane_dynamique,
    "dynamique_marche"
] = "Faible"


# ============================================================
# 6. PROFIL DE MARCHÉ
# ============================================================

df["profil_marche"] = (
    df["niveau_offre"]
    + " / "
    + df["dynamique_marche"]
)


# ============================================================
# 7. CONCENTRATION
# ============================================================

df["concentration"] = pd.NA

df.loc[
    df["cr5_pct"].notna()
    & (df["cr5_pct"] >= mediane_cr5),
    "concentration"
] = "Forte"

df.loc[
    df["cr5_pct"].notna()
    & (df["cr5_pct"] < mediane_cr5),
    "concentration"
] = "Faible"


# ============================================================
# 8. ORDRE DES COLONNES
# ============================================================

colonnes_signaux = [
    "niveau_offre",
    "dynamique_marche",
    "profil_marche",
    "concentration",
]

colonnes = [
    colonne
    for colonne in df.columns
    if colonne not in colonnes_signaux
]

# On place les signaux à la fin
df = df[
    colonnes + colonnes_signaux
]


# ============================================================
# 9. RÉSUMÉ
# ============================================================

print("\n" + "=" * 70)
print("RÉPARTITION DES PROFILS")
print("=" * 70)

print(
    df["profil_marche"]
    .value_counts()
    .to_string()
)


print("\n" + "=" * 70)
print("COMMUNES PAR PROFIL")
print("=" * 70)

print(
    df[
        [
            "commune",
            "actifs_pour_1000_habitants",
            "solde_pour_1000_hab",
            "profil_marche",
            "concentration",
        ]
    ]
    .sort_values(
        [
            "profil_marche",
            "actifs_pour_1000_habitants"
        ],
        ascending=[True, False]
    )
    .to_string(index=False)
)


# ============================================================
# 10. EXPORT
# ============================================================

df.to_csv(
    FICHIER_SORTIE,
    sep=";",
    index=False
)


print("\n" + "=" * 70)
print(
    f"Fichier créé : {FICHIER_SORTIE}"
)
print("=" * 70)