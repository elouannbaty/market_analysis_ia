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
    / "familles_lexicales_detectees.csv"
)

FICHIER_SORTIE = (
    BASE_DIR
    / "data"
    / "processed"
    / "familles_lexicales_par_categorie.csv"
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
# 3. FAMILLES
# ============================================================

familles = [
    "kebab",
    "cafe",
    "bar_tabac",
    "bistrot",
    "pizza",
    "burger_fast_food",
]


# ============================================================
# 4. ANALYSE
# ============================================================

resultats = []

for categorie, groupe in df.groupby("categorie"):

    total = len(groupe)

    for famille in familles:

        colonne = f"famille_{famille}"

        nombre = int(
            groupe[colonne].sum()
        )

        part = (
            nombre
            / total
            * 100
        )

        resultats.append(
            {
                "categorie": categorie,
                "famille": famille,
                "nombre": nombre,
                "part_pct": round(part, 2),
                "total_categorie": total,
            }
        )


resultats = pd.DataFrame(resultats)


# ============================================================
# 5. AFFICHAGE
# ============================================================

print("=" * 70)
print("FAMILLES LEXICALES PAR CATÉGORIE")
print("=" * 70)

for categorie in resultats["categorie"].unique():

    print(f"\n{categorie}")
    print("-" * 50)

    sous_table = (
        resultats[
            resultats["categorie"] == categorie
        ]
        .sort_values(
            "part_pct",
            ascending=False
        )
    )

    for _, ligne in sous_table.iterrows():

        print(
            f"{ligne['famille']:<20} "
            f"{ligne['nombre']:>4} "
            f"({ligne['part_pct']:>5.2f} %)"
        )


# ============================================================
# 6. EXPORT
# ============================================================

resultats.to_csv(
    FICHIER_SORTIE,
    sep=";",
    index=False
)


print("\n" + "=" * 70)
print(
    f"Fichier créé : {FICHIER_SORTIE}"
)
print("=" * 70)