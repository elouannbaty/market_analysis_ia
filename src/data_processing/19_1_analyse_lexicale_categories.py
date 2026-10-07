from pathlib import Path

import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer


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
    / "frequence_mots_par_categorie.csv"
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
# 3. PRÉPARATION
# ============================================================

df = df[
    df["enseigne_propre"].notna()
].copy()

df["texte_nlp"] = (
    df["enseigne_propre"]
    .astype(str)
    .str.strip()
)


# ============================================================
# 4. MOTS VIDES
# ============================================================

mots_vides = [
    "le",
    "la",
    "les",
    "de",
    "du",
    "des",
    "et",
    "a",
    "au",
    "aux",
    "en",
    "un",
    "une",
    "chez",
    "dans",
    "sur",
    "par",
    "pour",
    "avec",
    "sans",
    "sarl",
    "sas",
    "eurl",
    "sci",
    "sa",
    "ste",
    "societe",
    "société",
    "entreprise",
    "restauration",
]


# ============================================================
# 5. ANALYSE PAR CATÉGORIE
# ============================================================

resultats = []

categories = [
    "Restaurant",
    "Restauration rapide",
    "Café et bar",
]


for categorie in categories:

    df_cat = df[
        df["categorie"] == categorie
    ].copy()

    if len(df_cat) == 0:
        continue

    vectorizer = CountVectorizer(
        lowercase=True,
        strip_accents="unicode",
        stop_words=mots_vides,
        token_pattern=r"(?u)\b[a-zA-ZÀ-ÿ][a-zA-ZÀ-ÿ0-9]+\b",
        ngram_range=(1, 1),
        min_df=2
    )

    matrice = vectorizer.fit_transform(
        df_cat["texte_nlp"]
    )

    mots = vectorizer.get_feature_names_out()

    frequences = matrice.sum(axis=0).A1

    analyse = pd.DataFrame(
        {
            "categorie": categorie,
            "mot": mots,
            "nombre_etablissements": frequences,
        }
    )

    analyse["part_categorie"] = (
        analyse["nombre_etablissements"]
        / len(df_cat)
        * 100
    )

    analyse = analyse.sort_values(
        "nombre_etablissements",
        ascending=False
    )

    analyse["rang"] = range(1, len(analyse) + 1)

    resultats.append(analyse)


# ============================================================
# 6. CONSOLIDATION
# ============================================================

resultats = pd.concat(
    resultats,
    ignore_index=True
)


resultats = resultats[
    [
        "categorie",
        "rang",
        "mot",
        "nombre_etablissements",
        "part_categorie",
    ]
]


# ============================================================
# 7. EXPORT
# ============================================================

resultats.to_csv(
    FICHIER_SORTIE,
    sep=";",
    index=False
)


# ============================================================
# 8. AFFICHAGE
# ============================================================

print("=" * 70)
print("ANALYSE LEXICALE PAR CATÉGORIE")
print("=" * 70)


for categorie in categories:

    print(f"\n\n{'-' * 70}")
    print(f"{categorie.upper()}")
    print(f"{'-' * 70}")

    print(
        resultats[
            resultats["categorie"] == categorie
        ][
            [
                "rang",
                "mot",
                "nombre_etablissements",
                "part_categorie",
            ]
        ]
        .head(20)
        .to_string(index=False)
    )


print("\n" + "=" * 70)

print(
    f"Fichier créé : {FICHIER_SORTIE}"
)

print("=" * 70)