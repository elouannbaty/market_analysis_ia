from pathlib import Path

import pandas as pd


# ============================================================
# 1. PARAMÈTRES
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[2]

FICHIER_SIRENE = (
    BASE_DIR
    / "data"
    / "processed"
    / "table_analytique_restauration.csv"
)

FICHIER_SORTIE_ENTREPRISES = (
    BASE_DIR
    / "data"
    / "processed"
    / "analyse_entreprises_restauration.csv"
)

FICHIER_SORTIE_ENSEIGNES = (
    BASE_DIR
    / "data"
    / "processed"
    / "analyse_enseignes_restauration.csv"
)


# ============================================================
# 2. CHARGEMENT
# ============================================================

df = pd.read_csv(
    FICHIER_SIRENE,
    sep=";",
    low_memory=False
)

print("\nCOLONNES DISPONIBLES :")
print(df.columns.tolist())


# ============================================================
# 3. NORMALISATION
# ============================================================

df["siren"] = (
    df["siren"]
    .astype(str)
    .str.replace(".0", "", regex=False)
    .str.zfill(9)
)

df["siret"] = (
    df["siret"]
    .astype(str)
    .str.replace(".0", "", regex=False)
)

df["est_ferme"] = (
    df["est_ferme"]
    .astype(bool)
)


# ============================================================
# 4. ANALYSE DES ENTREPRISES / SIREN
# ============================================================

entreprises = (
    df
    .groupby("siren")
    .agg(
        nombre_etablissements=(
            "siret",
            "count"
        ),

        nombre_actifs=(
            "est_ferme",
            lambda x: (~x).sum()
        ),

        nombre_fermes=(
            "est_ferme",
            "sum"
        ),

        categories=(
            "categorie",
            lambda x: ", ".join(
                sorted(x.dropna().unique())
            )
        ),

        communes=(
            "commune",
            lambda x: ", ".join(
                sorted(x.dropna().unique())
            )
        )
    )
    .reset_index()
)


# ============================================================
# 5. TYPE D'ACTEUR
# ============================================================

entreprises["type_acteur"] = "Mono-établissement"

entreprises.loc[
    entreprises["nombre_etablissements"] > 1,
    "type_acteur"
] = "Multi-établissements"


# ============================================================
# 6. CLASSEMENT DES ENTREPRISES
# ============================================================

entreprises = entreprises.sort_values(
    [
        "nombre_etablissements",
        "nombre_actifs"
    ],
    ascending=False
)


entreprises["rang"] = (
    entreprises["nombre_etablissements"]
    .rank(
        ascending=False,
        method="min"
    )
    .astype(int)
)


# ============================================================
# 7. ANALYSE DES ENSEIGNES
# ============================================================

# On conserve uniquement les enseignes renseignées.

enseignes = df[
    df["enseigne_1"]
    .notna()
].copy()


enseignes["enseigne_1"] = (
    enseignes["enseigne_1"]
    .astype(str)
    .str.strip()
)


enseignes = enseignes[
    enseignes["enseigne_1"] != ""
]


# ============================================================
# 8. AGRÉGATION DES ENSEIGNES
# ============================================================

analyse_enseignes = (
    enseignes
    .groupby("enseigne_1")
    .agg(
        nombre_etablissements=(
            "siret",
            "nunique"
        ),

        nombre_entreprises=(
            "siren",
            "nunique"
        ),

        nombre_communes=(
            "commune",
            "nunique"
        ),

        actifs=(
            "est_ferme",
            lambda x: (~x).sum()
        ),

        fermes=(
            "est_ferme",
            "sum"
        ),

        categorie_principale=(
            "categorie",
            lambda x: x.mode().iloc[0]
            if not x.mode().empty
            else "Inconnue"
        )
    )
    .reset_index()
)


# ============================================================
# 9. PART D'ACTIFS
# ============================================================

analyse_enseignes["part_actifs"] = (
    analyse_enseignes["actifs"]
    / analyse_enseignes["nombre_etablissements"]
    * 100
)


# ============================================================
# 10. CLASSEMENT DES ENSEIGNES
# ============================================================

analyse_enseignes = (
    analyse_enseignes
    .sort_values(
        [
            "nombre_etablissements",
            "actifs"
        ],
        ascending=False
    )
)


analyse_enseignes["rang"] = (
    analyse_enseignes["nombre_etablissements"]
    .rank(
        ascending=False,
        method="min"
    )
    .astype(int)
)


# ============================================================
# 11. EXPORT DES DEUX TABLES
# ============================================================

entreprises.to_csv(
    FICHIER_SORTIE_ENTREPRISES,
    sep=";",
    index=False
)


analyse_enseignes.to_csv(
    FICHIER_SORTIE_ENSEIGNES,
    sep=";",
    index=False
)


# ============================================================
# 12. STATISTIQUES GÉNÉRALES
# ============================================================

nombre_entreprises = len(entreprises)

nombre_mono = (
    entreprises["type_acteur"]
    .eq("Mono-établissement")
    .sum()
)

nombre_multi = (
    entreprises["type_acteur"]
    .eq("Multi-établissements")
    .sum()
)

etablissements_multi = (
    entreprises.loc[
        entreprises["type_acteur"]
        == "Multi-établissements",
        "nombre_etablissements"
    ]
    .sum()
)


# ============================================================
# 13. AFFICHAGE
# ============================================================

print("=" * 70)
print("ANALYSE DES ACTEURS DU MARCHÉ")
print("=" * 70)

print(
    f"\nEntreprises / SIREN : "
    f"{nombre_entreprises}"
)

print(
    f"Mono-établissement : "
    f"{nombre_mono}"
)

print(
    f"Multi-établissements : "
    f"{nombre_multi}"
)

print(
    f"Établissements appartenant à "
    f"des entreprises multi-établissements : "
    f"{etablissements_multi}"
)


print("\nTop 15 des entreprises par nombre d'établissements :")

print(
    entreprises[
        [
            "siren",
            "nombre_etablissements",
            "nombre_actifs",
            "nombre_fermes",
            "type_acteur",
            "categories",
            "communes"
        ]
    ]
    .head(15)
    .to_string(index=False)
)


print("\nTop 20 des enseignes :")

print(
    analyse_enseignes[
        [
            "enseigne_1",
            "nombre_etablissements",
            "nombre_entreprises",
            "nombre_communes",
            "actifs",
            "fermes",
            "part_actifs",
            "categorie_principale"
        ]
    ]
    .head(20)
    .to_string(index=False)
)


print("\n" + "=" * 70)
print(
    f"Fichier entreprises : "
    f"{FICHIER_SORTIE_ENTREPRISES}"
)

print(
    f"Fichier enseignes : "
    f"{FICHIER_SORTIE_ENSEIGNES}"
)

print("=" * 70)