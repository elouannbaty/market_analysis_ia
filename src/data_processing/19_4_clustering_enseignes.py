from pathlib import Path

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans


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
    / "clustering_enseignes_restauration.csv"
)

NOMBRE_CLUSTERS = 6


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
    .str.strip()
)


# ============================================================
# 4. STOPWORDS
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
# 5. TF-IDF
# ============================================================

vectorizer = TfidfVectorizer(
    lowercase=True,
    strip_accents="unicode",
    stop_words=mots_vides,
    token_pattern=r"(?u)\b[a-zA-ZÀ-ÿ][a-zA-ZÀ-ÿ0-9]+\b",
    ngram_range=(1, 2),
    min_df=2
)


X = vectorizer.fit_transform(
    df["texte_nlp"]
)


termes = vectorizer.get_feature_names_out()


# ============================================================
# 6. CLUSTERING K-MEANS
# ============================================================

kmeans = KMeans(
    n_clusters=NOMBRE_CLUSTERS,
    n_init=20,
    random_state=42
)


df["cluster"] = kmeans.fit_predict(X)


# ============================================================
# 7. TAILLE DES CLUSTERS
# ============================================================

tailles = (
    df["cluster"]
    .value_counts()
    .sort_index()
)


# ============================================================
# 8. TERMES DOMINANTS DE CHAQUE CLUSTER
# ============================================================

print("=" * 70)
print("CLUSTERING DES ENSEIGNES")
print("=" * 70)

print(
    f"\nNombre d'enseignes analysées : {len(df)}"
)

print(
    f"Nombre de clusters : {NOMBRE_CLUSTERS}"
)


print("\nTaille des clusters :")

for cluster, taille in tailles.items():

    part = (
        taille
        / len(df)
        * 100
    )

    print(
        f"Cluster {cluster} : "
        f"{taille} enseignes "
        f"({part:.2f} %)"
    )


print("\nTermes dominants par cluster :")


centroides = kmeans.cluster_centers_


for cluster in range(NOMBRE_CLUSTERS):

    scores = centroides[cluster]

    indices = scores.argsort()[::-1][:15]

    termes_dominants = [
        termes[i]
        for i in indices
    ]

    print(
        f"\nCluster {cluster} :"
    )

    print(
        ", ".join(termes_dominants)
    )


# ============================================================
# 9. EXEMPLES D'ENSEIGNES PAR CLUSTER
# ============================================================

print("\n\nExemples d'enseignes par cluster :")


for cluster in range(NOMBRE_CLUSTERS):

    exemples = (
        df[
            df["cluster"] == cluster
        ]["enseigne_propre"]
        .head(15)
        .tolist()
    )

    print(
        f"\nCluster {cluster} :"
    )

    print(
        " | ".join(exemples)
    )


# ============================================================
# 10. EXPORT
# ============================================================

colonnes_sortie = [
    "siret",
    "commune",
    "categorie",
    "enseigne_propre",
    "cluster",
]


df[
    colonnes_sortie
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