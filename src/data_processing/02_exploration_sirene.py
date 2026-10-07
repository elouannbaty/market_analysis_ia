from pathlib import Path
import pandas as pd


DATA_FILE = (
    Path(__file__).resolve().parents[2]
    / "data"
    / "raw"
    / "sirene_nantes_metropole.csv"
)


df = pd.read_csv(
    DATA_FILE,
    sep=";",
    low_memory=False
)

print("Dimensions du fichier :")
print(df.shape)

print("\nColonnes :")
for column in df.columns:
    print(column)

print("\nPremières lignes :")
print(df.head())

print("\nPrincipaux codes NAF :")
print(
    df["activiteprincipaleetablissement"]
    .value_counts(dropna=False)
    .head(30)
)

codes_restauration = [
    "56.10A",
    "56.10B",
    "56.10C",
    "56.30Z",
]

print("\nÉtablissements du périmètre restauration :")

print(
    df[
        "activiteprincipaleetablissement"
    ].isin(codes_restauration).value_counts()
)

print("\nRépartition par code NAF :")

print(
    df[
        df["activiteprincipaleetablissement"].isin(codes_restauration)
    ]["activiteprincipaleetablissement"]
    .value_counts()
    .sort_index()
)

restaurants = df[
    df["activiteprincipaleetablissement"].isin(codes_restauration)
].copy()

print("\nStatut administratif des établissements de restauration :")

print(
    restaurants["etatadministratifetablissement"]
    .value_counts(dropna=False)
)

print("\nDates de création :")
print(
    restaurants["datecreationetablissement"]
    .describe()
)

print("\nDates de fermeture :")
print(
    restaurants["datefermetureetablissement"]
    .describe()
)

print("\nNombre de dates de fermeture renseignées :")
print(
    restaurants["datefermetureetablissement"]
    .notna()
    .sum()
)

print("\nDates de création les plus anciennes :")
print(
    restaurants["datecreationetablissement"]
    .sort_values()
    .head(30)
    .to_list()
)