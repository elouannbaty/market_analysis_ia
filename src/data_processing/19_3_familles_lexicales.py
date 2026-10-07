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
    / "familles_lexicales_restauration.csv"
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
# 3. SÉLECTION DES ENSEIGNES
# ============================================================

df = df[
    df["enseigne_propre"].notna()
].copy()

df["texte_nlp"] = (
    df["enseigne_propre"]
    .astype(str)
    .str.lower()
)


# ============================================================
# 4. DÉFINITION DES FAMILLES LEXICALES
# ============================================================

familles = {

    "Pizza / pizzeria": [
        "pizza",
        "pizzeria",
        "pizz",
    ],

    "Burger / fast-food": [
        "burger",
        "hamburger",
        "fast",
        "food",
        "chicken",
        "express",
    ],

    "Cuisine internationale / street-food": [
        "kebab",
        "tacos",
        "sushi",
        "wok",
        "thai",
        "indien",
        "indienne",
        "japon",
        "japonais",
        "japonaise",
        "mexicain",
        "mexicaine",
        "orient",
        "libanais",
        "libanaise",
    ],

    "Café / bar": [
        "cafe",
        "café",
        "bar",
        "bistrot",
        "bistro",
        "pub",
        "brasserie",
        "coffee",
        "biere",
        "bières",
    ],

    "Restauration traditionnelle": [
        "restaurant",
        "resto",
        "creperie",
        "crêperie",
        "grill",
        "cuisine",
        "gourmand",
        "gourmande",
        "maison",
        "saveurs",
        "comptoir",
        "table",
    ],
}


# ============================================================
# 5. DÉTECTION DES FAMILLES
# ============================================================

for famille, termes in familles.items():

    nom_colonne = (
        "famille_"
        + famille
        .lower()
        .replace(" / ", "_")
        .replace(" ", "_")
        .replace("-", "_")
        .replace("é", "e")
        .replace("è", "e")
        .replace("ê", "e")
        .replace("à", "a")
        .replace("û", "u")
    )

    df[nom_colonne] = False

    for terme in termes:

        df[nom_colonne] = (
            df[nom_colonne]
            | df["texte_nlp"].str.contains(
                terme,
                regex=False,
                na=False
            )
        )


# ============================================================
# 6. NOMBRE DE FAMILLES PAR ENSEIGNE
# ============================================================

colonnes_familles = [
    colonne
    for colonne in df.columns
    if colonne.startswith("famille_")
]


df["nombre_familles_lexicales"] = (
    df[colonnes_familles]
    .sum(axis=1)
)


# ============================================================
# 7. FAMILLE(S) IDENTIFIÉE(S)
# ============================================================

def construire_liste_familles(row):

    familles_trouvees = []

    for colonne in colonnes_familles:

        if row[colonne]:

            nom = colonne.replace(
                "famille_",
                ""
            )

            familles_trouvees.append(nom)

    return " | ".join(familles_trouvees)


df["familles_lexicales"] = df.apply(
    construire_liste_familles,
    axis=1
)


# ============================================================
# 8. INDICATEUR AUTRE
# ============================================================

df["famille_autre"] = (
    df["nombre_familles_lexicales"] == 0
)


# ============================================================
# 9. EXPORT
# ============================================================

colonnes_sortie = [
    "siret",
    "commune",
    "categorie",
    "enseigne_propre",
    "familles_lexicales",
    "nombre_familles_lexicales",
    "famille_autre",
]

colonnes_sortie += colonnes_familles


resultat = df[colonnes_sortie].copy()


resultat.to_csv(
    FICHIER_SORTIE,
    sep=";",
    index=False
)


# ============================================================
# 10. STATISTIQUES
# ============================================================

print("=" * 70)
print("FAMILLES LEXICALES DES ENSEIGNES")
print("=" * 70)

print(
    f"\nÉtablissements analysés : {len(df)}"
)


print("\nNombre d'établissements par famille :")

for colonne in colonnes_familles:

    nombre = int(
        df[colonne].sum()
    )

    part = (
        nombre
        / len(df)
        * 100
    )

    nom = colonne.replace(
        "famille_",
        ""
    )

    print(
        f"{nom:<45} "
        f"{nombre:>5} "
        f"({part:.2f} %)"
    )


nombre_autre = int(
    df["famille_autre"].sum()
)

part_autre = (
    nombre_autre
    / len(df)
    * 100
)

print(
    f"{'Autre / non identifié':<45} "
    f"{nombre_autre:>5} "
    f"({part_autre:.2f} %)"
)


print("\nRépartition par nombre de familles :")

print(
    df["nombre_familles_lexicales"]
    .value_counts()
    .sort_index()
    .to_string()
)


# ============================================================
# 11. EXEMPLES
# ============================================================

print("\nExemples d'enseignes avec familles identifiées :")

print(
    resultat[
        resultat["nombre_familles_lexicales"] > 0
    ][
        [
            "enseigne_propre",
            "categorie",
            "familles_lexicales"
        ]
    ]
    .head(30)
    .to_string(index=False)
)


print("\n" + "=" * 70)

print(
    f"Fichier créé : {FICHIER_SORTIE}"
)

print("=" * 70)