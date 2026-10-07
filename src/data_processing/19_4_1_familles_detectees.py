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
    / "noms_commerciaux_restauration.csv"
)

FICHIER_SORTIE = (
    BASE_DIR
    / "data"
    / "processed"
    / "familles_lexicales_detectees.csv"
)


# ============================================================
# 2. CHARGEMENT
# ============================================================

df = pd.read_csv(
    FICHIER_SOURCE,
    sep=";",
    low_memory=False
)

df = df[
    df["enseigne_propre"].notna()
].copy()

df["texte"] = (
    df["enseigne_propre"]
    .astype(str)
    .str.lower()
    .str.strip()
)


# ============================================================
# 3. DÉFINITION DES FAMILLES
# ============================================================

familles = {

    "kebab": [
        "kebab",
        "doner",
        "döner"
    ],

    "cafe": [
        "cafe",
        "coffee"
    ],

    "bar_tabac": [
        "bar",
        "tabac",
        "pub"
    ],

    "bistrot": [
        "bistrot",
        "bistro"
    ],

    "pizza": [
        "pizza",
        "pizzeria",
        "pizz"
    ],

    "burger_fast_food": [
        "burger",
        "hamburger",
        "fast food",
        "fast-food"
    ],
}


# ============================================================
# 4. DÉTECTION
# ============================================================

for famille, termes in familles.items():

    colonne = f"famille_{famille}"

    df[colonne] = df["texte"].apply(
        lambda x: any(
            terme in x
            for terme in termes
        )
    )


# ============================================================
# 5. NOMBRE DE FAMILLES PAR ENSEIGNE
# ============================================================

colonnes_familles = [
    f"famille_{famille}"
    for famille in familles
]

df["nombre_familles"] = (
    df[colonnes_familles]
    .sum(axis=1)
)


df["famille_detectee"] = (
    df[colonnes_familles]
    .apply(
        lambda ligne: ", ".join(
            famille
            for famille, valeur in zip(
                familles.keys(),
                ligne
            )
            if valeur
        ),
        axis=1
    )
)


# ============================================================
# 6. RÉSULTATS
# ============================================================

print("=" * 70)
print("FAMILLES LEXICALES DÉTECTÉES")
print("=" * 70)

print(
    f"\nEnseignes analysées : {len(df)}"
)


for famille in familles:

    colonne = f"famille_{famille}"

    nombre = int(
        df[colonne].sum()
    )

    part = (
        nombre
        / len(df)
        * 100
    )

    print(
        f"{famille:<20} "
        f"{nombre:>4} "
        f"({part:>5.2f} %)"
    )


# ============================================================
# 7. COMBINAISONS
# ============================================================

print("\n" + "=" * 70)
print("COMBINAISONS DE FAMILLES")
print("=" * 70)

combinaisons = (
    df["famille_detectee"]
    .replace("", "Aucune famille")
    .value_counts()
)

print(
    combinaisons.head(20)
)


# ============================================================
# 8. EXEMPLES
# ============================================================

print("\n" + "=" * 70)
print("EXEMPLES")
print("=" * 70)


for famille in familles:

    colonne = f"famille_{famille}"

    exemples = (
        df[
            df[colonne]
        ]["enseigne_propre"]
        .head(10)
        .tolist()
    )

    print(
        f"\n{famille} :"
    )

    print(
        " | ".join(exemples)
    )


# ============================================================
# 9. EXPORT
# ============================================================

colonnes_export = [
    "siret",
    "commune",
    "categorie",
    "enseigne_propre",
    *colonnes_familles,
    "nombre_familles",
    "famille_detectee",
]


df[
    colonnes_export
].to_csv(
    FICHIER_SORTIE,
    sep=";",
    index=False
)


print("\n" + "=" * 70)
print(
    f"Fichier créé : {FICHIER_SORTIE}"
)
print("=" * 70)