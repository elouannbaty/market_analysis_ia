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

FICHIER_SORTIE_MOTS = (
    BASE_DIR
    / "data"
    / "processed"
    / "frequence_mots_restauration.csv"
)

FICHIER_SORTIE_BIGRAMMES = (
    BASE_DIR
    / "data"
    / "processed"
    / "frequence_bigrammes_restauration.csv"
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

df_nlp = df[
    df["enseigne_propre"].notna()
].copy()

df_nlp["texte_nlp"] = (
    df_nlp["enseigne_propre"]
    .astype(str)
    .str.strip()
)


print("=" * 70)
print("ANALYSE LEXICALE DU MARCHÉ")
print("=" * 70)

print(
    f"\nÉtablissements avec enseigne renseignée : "
    f"{len(df_nlp)}"
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
# 5. ANALYSE DES MOTS
# ============================================================

vectorizer_mots = CountVectorizer(
    lowercase=True,
    strip_accents="unicode",
    stop_words=mots_vides,
    token_pattern=r"(?u)\b[a-zA-ZÀ-ÿ][a-zA-ZÀ-ÿ0-9]+\b",
    ngram_range=(1, 1),
    min_df=2
)


matrice_mots = vectorizer_mots.fit_transform(
    df_nlp["texte_nlp"]
)

mots = vectorizer_mots.get_feature_names_out()

frequences = matrice_mots.sum(axis=0).A1


analyse_mots = pd.DataFrame(
    {
        "mot": mots,
        "nombre_etablissements": frequences
    }
)


analyse_mots = (
    analyse_mots
    .sort_values(
        "nombre_etablissements",
        ascending=False
    )
    .reset_index(drop=True)
)

analyse_mots["rang"] = (
    analyse_mots.index + 1
)

analyse_mots["part_enseignes"] = (
    analyse_mots["nombre_etablissements"]
    / len(df_nlp)
    * 100
)


# ============================================================
# 6. ANALYSE DES BIGRAMMES
# ============================================================

vectorizer_bigrammes = CountVectorizer(
    lowercase=True,
    strip_accents="unicode",
    stop_words=mots_vides,
    token_pattern=r"(?u)\b[a-zA-ZÀ-ÿ][a-zA-ZÀ-ÿ0-9]+\b",
    ngram_range=(2, 2),
    min_df=2
)


matrice_bigrammes = vectorizer_bigrammes.fit_transform(
    df_nlp["texte_nlp"]
)

bigrammes = (
    vectorizer_bigrammes
    .get_feature_names_out()
)

frequences_bigrammes = (
    matrice_bigrammes.sum(axis=0).A1
)


analyse_bigrammes = pd.DataFrame(
    {
        "bigramme": bigrammes,
        "nombre_etablissements": frequences_bigrammes
    }
)


analyse_bigrammes = (
    analyse_bigrammes
    .sort_values(
        "nombre_etablissements",
        ascending=False
    )
    .reset_index(drop=True)
)

analyse_bigrammes["rang"] = (
    analyse_bigrammes.index + 1
)

analyse_bigrammes["part_enseignes"] = (
    analyse_bigrammes["nombre_etablissements"]
    / len(df_nlp)
    * 100
)


# ============================================================
# 7. EXPORTS
# ============================================================

analyse_mots.to_csv(
    FICHIER_SORTIE_MOTS,
    sep=";",
    index=False
)

analyse_bigrammes.to_csv(
    FICHIER_SORTIE_BIGRAMMES,
    sep=";",
    index=False
)


# ============================================================
# 8. AFFICHAGE
# ============================================================

print(
    f"\nNombre de mots retenus : "
    f"{len(analyse_mots)}"
)

print(
    f"Nombre de bigrammes retenus : "
    f"{len(analyse_bigrammes)}"
)


print("\nTop 30 des mots :")

print(
    analyse_mots[
        [
            "rang",
            "mot",
            "nombre_etablissements",
            "part_enseignes"
        ]
    ]
    .head(30)
    .to_string(index=False)
)


print("\nTop 30 des bigrammes :")

print(
    analyse_bigrammes[
        [
            "rang",
            "bigramme",
            "nombre_etablissements",
            "part_enseignes"
        ]
    ]
    .head(30)
    .to_string(index=False)
)


print("\n" + "=" * 70)

print(
    f"Fichier mots : "
    f"{FICHIER_SORTIE_MOTS}"
)

print(
    f"Fichier bigrammes : "
    f"{FICHIER_SORTIE_BIGRAMMES}"
)

print("=" * 70)