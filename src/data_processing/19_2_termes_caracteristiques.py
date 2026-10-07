from pathlib import Path

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer


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
    / "termes_caracteristiques_categories.csv"
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
# 5. AGRÉGATION PAR CATÉGORIE
# ============================================================

corpus = (
    df
    .groupby("categorie")["texte_nlp"]
    .apply(lambda x: " ".join(x))
)


# ============================================================
# 6. TF-IDF
# ============================================================

vectorizer = TfidfVectorizer(
    lowercase=True,
    strip_accents="unicode",
    stop_words=mots_vides,
    token_pattern=r"(?u)\b[a-zA-ZÀ-ÿ][a-zA-ZÀ-ÿ0-9]+\b",
    ngram_range=(1, 2),
    min_df=2
)


matrice = vectorizer.fit_transform(corpus)


termes = vectorizer.get_feature_names_out()

categories = corpus.index.tolist()


# ============================================================
# 7. CONSTRUCTION DES RÉSULTATS
# ============================================================

resultats = []


for i, categorie in enumerate(categories):

    scores = matrice[i].toarray().flatten()

    analyse = pd.DataFrame(
        {
            "categorie": categorie,
            "terme": termes,
            "score_tfidf": scores
        }
    )

    analyse = analyse[
        analyse["score_tfidf"] > 0
    ].copy()

    analyse = analyse.sort_values(
        "score_tfidf",
        ascending=False
    )

    analyse["rang"] = range(
        1,
        len(analyse) + 1
    )

    resultats.append(analyse)


# ============================================================
# 8. CONSOLIDATION
# ============================================================

resultats = pd.concat(
    resultats,
    ignore_index=True
)


resultats = resultats[
    [
        "categorie",
        "rang",
        "terme",
        "score_tfidf"
    ]
]


# ============================================================
# 9. EXPORT
# ============================================================

resultats.to_csv(
    FICHIER_SORTIE,
    sep=";",
    index=False
)


# ============================================================
# 10. AFFICHAGE
# ============================================================

print("=" * 70)
print("TERMES CARACTÉRISTIQUES PAR CATÉGORIE")
print("=" * 70)


for categorie in categories:

    print(f"\n\n{'-' * 70}")
    print(categorie.upper())
    print(f"{'-' * 70}")

    print(
        resultats[
            resultats["categorie"] == categorie
        ][
            [
                "rang",
                "terme",
                "score_tfidf"
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