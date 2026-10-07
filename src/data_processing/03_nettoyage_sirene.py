from pathlib import Path

import pandas as pd


# ============================================================
# Chemins
# ============================================================

DATA_FILE = (
    Path(__file__).resolve().parents[2]
    / "data"
    / "raw"
    / "sirene_nantes_metropole.csv"
)

OUTPUT_DIR = (
    Path(__file__).resolve().parents[2]
    / "data"
    / "processed"
)

OUTPUT_FILE = OUTPUT_DIR / "sirene_restauration.csv"


# ============================================================
# Paramètres
# ============================================================

CODES_NAF_RESTAURATION = [
    "56.10A",
    "56.10B",
    "56.10C",
    "56.30Z",
]


# ============================================================
# Chargement
# ============================================================

print("Chargement de la base SIRENE...")

df = pd.read_csv(
    DATA_FILE,
    sep=";",
    low_memory=False
)

print(f"Base initiale : {df.shape[0]:,} établissements")


# ============================================================
# Filtre du périmètre restauration
# ============================================================

df = df[
    df["activiteprincipaleetablissement"]
    .isin(CODES_NAF_RESTAURATION)
].copy()

print(
    f"Établissements du périmètre restauration : "
    f"{df.shape[0]:,}"
)


# ============================================================
# Sélection des variables utiles
# ============================================================

columns_to_keep = [
    "siret",
    "siren",
    "nic",

    "etatadministratifetablissement",

    "datecreationetablissement",
    "datefermetureetablissement",

    "activiteprincipaleetablissement",
    "nomenclatureactiviteprincipaleetablissement",

    "sectionetablissement",
    "divisionetablissement",
    "groupeetablissement",
    "classeetablissement",

    "enseigne1etablissement",
    "enseigne2etablissement",
    "enseigne3etablissement",
    "denominationusuelleetablissement",

    "trancheeffectifsetablissement",
    "anneeeffectifsetablissement",
    "caractereemployeuretablissement",
    "categorieentreprise",

    "codepostaletablissement",
    "libellecommuneetablissement",
    "codecommuneetablissement",

    "adresseetablissement",

    "codeepcietablissement",
    "epcietablissement",

    "departementetablissement",
    "regionetablissement",

    "etablissementsiege",

    "geolocetablissement",
]

df = df[columns_to_keep].copy()


# ============================================================
# Nettoyage des dates
# ============================================================

df["datecreationetablissement"] = pd.to_datetime(
    df["datecreationetablissement"],
    errors="coerce"
)

df["datefermetureetablissement"] = pd.to_datetime(
    df["datefermetureetablissement"],
    errors="coerce"
)

# 01/01/1900 = date de création non renseignée
df.loc[
    df["datecreationetablissement"]
    == pd.Timestamp("1900-01-01"),
    "datecreationetablissement"
] = pd.NaT


# ============================================================
# Nettoyage de la géolocalisation
# ============================================================

def extract_coordinates(value):
    if pd.isna(value):
        return pd.Series([pd.NA, pd.NA])

    try:
        latitude, longitude = str(value).split(",")
        return pd.Series([
            float(latitude.strip()),
            float(longitude.strip())
        ])
    except (ValueError, AttributeError):
        return pd.Series([pd.NA, pd.NA])


df[
    ["latitude", "longitude"]
] = df["geolocetablissement"].apply(
    extract_coordinates
)


# ============================================================
# Renommage des variables
# ============================================================

df = df.rename(
    columns={
        "siret": "siret",
        "siren": "siren",
        "nic": "nic",

        "etatadministratifetablissement": "statut",

        "datecreationetablissement": "date_creation",
        "datefermetureetablissement": "date_fermeture",

        "activiteprincipaleetablissement": "code_naf",
        "nomenclatureactiviteprincipaleetablissement": "nomenclature_naf",

        "sectionetablissement": "section_naf",
        "divisionetablissement": "division_naf",
        "groupeetablissement": "groupe_naf",
        "classeetablissement": "classe_naf",

        "enseigne1etablissement": "enseigne_1",
        "enseigne2etablissement": "enseigne_2",
        "enseigne3etablissement": "enseigne_3",
        "denominationusuelleetablissement": "denomination",

        "trancheeffectifsetablissement": "tranche_effectif",
        "anneeeffectifsetablissement": "annee_effectif",
        "caractereemployeuretablissement": "employeur",
        "categorieentreprise": "categorie_entreprise",

        "codepostaletablissement": "code_postal",
        "libellecommuneetablissement": "commune",
        "codecommuneetablissement": "code_commune",

        "adresseetablissement": "adresse",

        "codeepcietablissement": "code_epci",
        "epcietablissement": "epci",

        "departementetablissement": "departement",
        "regionetablissement": "region",

        "etablissementsiege": "siege",

        "geolocetablissement": "geolocalisation",
    }
)


# ============================================================
# Création du dossier de sortie
# ============================================================

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# ============================================================
# Export
# ============================================================

df.to_csv(
    OUTPUT_FILE,
    sep=";",
    index=False
)


# ============================================================
# Résumé
# ============================================================

print("\nNettoyage terminé.")
print(f"Fichier créé : {OUTPUT_FILE}")
print(f"Nombre de lignes : {len(df):,}")
print(f"Nombre de colonnes : {len(df.columns)}")

print("\nRépartition par code NAF :")
print(
    df["code_naf"]
    .value_counts()
    .sort_index()
)

print("\nRépartition par statut :")
print(
    df["statut"]
    .value_counts(dropna=False)
)

print("\nDates de création manquantes :")
print(
    df["date_creation"]
    .isna()
    .sum()
)