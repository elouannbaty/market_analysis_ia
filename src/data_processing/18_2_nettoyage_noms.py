from pathlib import Path

import pandas as pd


# ============================================================
# 1. PARAMÈTRES
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[2]

FICHIER_SOURCE = (
    BASE_DIR
    / "data"
    / "processed"
    / "table_analytique_restauration.csv"
)

FICHIER_SORTIE = (
    BASE_DIR
    / "data"
    / "processed"
    / "noms_commerciaux_restauration.csv"
)


# ============================================================
# 2. CHARGEMENT
# ============================================================

df = pd.read_csv(
    FICHIER_SOURCE,
    sep=";",
    low_memory=False
)


# ============================================================
# 3. MARCHÉ ACTIF
# ============================================================

df = df[
    df["est_ferme"] == False
].copy()


# ============================================================
# 4. NETTOYAGE ENSEIGNE
# ============================================================

df["enseigne_propre"] = (
    df["enseigne_1"]
    .fillna("")
    .astype(str)
    .str.strip()
    .str.upper()
)


# Valeurs considérées comme non renseignées

valeurs_non_renseignees = [
    "",
    "[ND]",
    "ND",
    "N.D.",
    "NON RENSEIGNE",
    "NON RENSEIGNÉ",
    "NEANT",
    "NÉANT"
]

df.loc[
    df["enseigne_propre"].isin(valeurs_non_renseignees),
    "enseigne_propre"
] = pd.NA


# ============================================================
# 5. NETTOYAGE DENOMINATION
# ============================================================

df["denomination_propre"] = (
    df["denomination"]
    .fillna("")
    .astype(str)
    .str.strip()
    .str.upper()
)

df.loc[
    df["denomination_propre"].isin(valeurs_non_renseignees),
    "denomination_propre"
] = pd.NA


# ============================================================
# 6. INDICATEURS DE RENSEIGNEMENT
# ============================================================

df["enseigne_renseignee"] = (
    df["enseigne_propre"].notna()
)

df["denomination_renseignee"] = (
    df["denomination_propre"].notna()
)


# ============================================================
# 7. TYPE DE NOM DISPONIBLE
# ============================================================

df["type_nom"] = "Aucun nom"

df.loc[
    df["denomination_renseignee"],
    "type_nom"
] = "Dénomination"

df.loc[
    df["enseigne_renseignee"],
    "type_nom"
] = "Enseigne"

df.loc[
    df["enseigne_renseignee"]
    & df["denomination_renseignee"],
    "type_nom"
] = "Enseigne + dénomination"


# ============================================================
# 8. TABLE FINALE
# ============================================================

resultat = df[
    [
        "siret",
        "siren",
        "categorie",
        "commune",
        "code_commune",
        "enseigne_propre",
        "denomination_propre",
        "enseigne_renseignee",
        "denomination_renseignee",
        "type_nom"
    ]
].copy()


# ============================================================
# 9. EXPORT
# ============================================================

resultat.to_csv(
    FICHIER_SORTIE,
    sep=";",
    index=False
)


# ============================================================
# 10. STATISTIQUES
# ============================================================

nombre_total = len(resultat)

nombre_enseignes = (
    resultat["enseigne_renseignee"]
    .sum()
)

nombre_denominations = (
    resultat["denomination_renseignee"]
    .sum()
)

nombre_les_deux = (
    (
        resultat["enseigne_renseignee"]
        & resultat["denomination_renseignee"]
    )
    .sum()
)

part_enseignes = (
    nombre_enseignes
    / nombre_total
    * 100
)

part_denominations = (
    nombre_denominations
    / nombre_total
    * 100
)

part_les_deux = (
    nombre_les_deux
    / nombre_total
    * 100
)


# ============================================================
# 11. TOP ENSEIGNES APRÈS NETTOYAGE
# ============================================================

top_enseignes = (
    resultat[
        resultat["enseigne_renseignee"]
    ]
    .groupby("enseigne_propre")
    .agg(
        etablissements=("siret", "nunique"),
        entreprises=("siren", "nunique"),
        communes=("commune", "nunique")
    )
    .reset_index()
    .sort_values(
        "etablissements",
        ascending=False
    )
)


# ============================================================
# 12. AFFICHAGE
# ============================================================

print("=" * 70)
print("NETTOYAGE DES NOMS COMMERCIAUX")
print("=" * 70)

print(
    f"\nÉtablissements actifs : "
    f"{nombre_total}"
)

print(
    f"Enseignes renseignées : "
    f"{nombre_enseignes} "
    f"({part_enseignes:.2f} %)"
)

print(
    f"Dénominations renseignées : "
    f"{nombre_denominations} "
    f"({part_denominations:.2f} %)"
)

print(
    f"Enseigne + dénomination : "
    f"{nombre_les_deux} "
    f"({part_les_deux:.2f} %)"
)


print("\nRépartition du type de nom :")

print(
    resultat["type_nom"]
    .value_counts()
    .to_string()
)


print("\nTop 20 des enseignes après nettoyage :")

print(
    top_enseignes
    .head(20)
    .to_string(index=False)
)


print("\n" + "=" * 70)
print(
    f"Fichier créé : {FICHIER_SORTIE}"
)
print("=" * 70)