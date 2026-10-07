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
    / "dynamique_restauration_commune.csv"
)


# ============================================================
# 2. CHARGEMENT DES DONNÉES
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
# 3. PRÉPARATION DES CODES COMMUNES
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
# 5. FILTRE SUR LA PÉRIODE RÉCENTE
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
# 6. AGRÉGATION DES CRÉATIONS
# ============================================================

creations_commune = (
    creations
    .groupby("code_commune")
    .size()
    .reset_index(name="creations_2022_2025")
)


# ============================================================
# 7. AGRÉGATION DES FERMETURES
# ============================================================

fermetures_commune = (
    fermetures
    .groupby("code_commune")
    .size()
    .reset_index(name="fermetures_2022_2025")
)


# ============================================================
# 8. FUSION CRÉATIONS / FERMETURES
# ============================================================

dynamique = territoires[
    [
        "code_commune",
        "commune",
        "population_2023"
    ]
].copy()

dynamique = dynamique.merge(
    creations_commune,
    on="code_commune",
    how="left"
)

dynamique = dynamique.merge(
    fermetures_commune,
    on="code_commune",
    how="left"
)


# ============================================================
# 9. REMPLACEMENT DES VALEURS MANQUANTES
# ============================================================

dynamique["creations_2022_2025"] = (
    dynamique["creations_2022_2025"]
    .fillna(0)
    .astype(int)
)

dynamique["fermetures_2022_2025"] = (
    dynamique["fermetures_2022_2025"]
    .fillna(0)
    .astype(int)
)


# ============================================================
# 10. SOLDE DU MARCHÉ
# ============================================================

dynamique["solde_2022_2025"] = (
    dynamique["creations_2022_2025"]
    - dynamique["fermetures_2022_2025"]
)


# ============================================================
# 11. INDICATEURS RAPPORTÉS À LA POPULATION
# ============================================================

dynamique["creations_pour_1000_habitants"] = (
    dynamique["creations_2022_2025"]
    / dynamique["population_2023"]
    * 1000
)

dynamique["fermetures_pour_1000_habitants"] = (
    dynamique["fermetures_2022_2025"]
    / dynamique["population_2023"]
    * 1000
)

dynamique["solde_pour_1000_habitants"] = (
    dynamique["solde_2022_2025"]
    / dynamique["population_2023"]
    * 1000
)


# ============================================================
# 12. CLASSEMENT PAR DYNAMIQUE NETTE
# ============================================================

dynamique["rang_dynamique_nette"] = (
    dynamique["solde_pour_1000_habitants"]
    .rank(
        ascending=False,
        method="min"
    )
    .astype(int)
)


# ============================================================
# 13. ARRONDIS
# ============================================================

colonnes_arrondir = [
    "creations_pour_1000_habitants",
    "fermetures_pour_1000_habitants",
    "solde_pour_1000_habitants"
]

dynamique[colonnes_arrondir] = (
    dynamique[colonnes_arrondir]
    .round(2)
)


# ============================================================
# 14. TRI
# ============================================================

dynamique = dynamique.sort_values(
    "solde_pour_1000_habitants",
    ascending=False
)


# ============================================================
# 15. EXPORT
# ============================================================

dynamique.to_csv(
    FICHIER_SORTIE,
    sep=";",
    index=False
)


# ============================================================
# 16. CONTRÔLES
# ============================================================

print("=" * 60)
print("ANALYSE DE LA DYNAMIQUE DU MARCHÉ")
print("=" * 60)

print(f"\nPériode étudiée : {ANNEE_DEBUT}–{ANNEE_FIN}")

print(f"\nNombre de communes : {len(dynamique)}")

print(
    f"\nCréations enregistrées : "
    f"{dynamique['creations_2022_2025'].sum():,}"
    .replace(",", " ")
)

print(
    f"Fermetures enregistrées : "
    f"{dynamique['fermetures_2022_2025'].sum():,}"
    .replace(",", " ")
)

print(
    f"Solde total : "
    f"{dynamique['solde_2022_2025'].sum():,}"
    .replace(",", " ")
)

print("\nTop 10 des communes par dynamique nette :")

print(
    dynamique[
        [
            "commune",
            "creations_2022_2025",
            "fermetures_2022_2025",
            "solde_2022_2025",
            "creations_pour_1000_habitants",
            "fermetures_pour_1000_habitants",
            "solde_pour_1000_habitants"
        ]
    ]
    .head(10)
    .to_string(index=False)
)

print("\n" + "=" * 60)
print(f"Fichier créé : {FICHIER_SORTIE}")
print("=" * 60)