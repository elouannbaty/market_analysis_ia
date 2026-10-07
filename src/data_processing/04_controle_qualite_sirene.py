from pathlib import Path

import pandas as pd


# ============================================================
# Chemins
# ============================================================

DATA_FILE = (
    Path(__file__).resolve().parents[2]
    / "data"
    / "processed"
    / "sirene_restauration.csv"
)


# ============================================================
# Chargement
# ============================================================

print("Chargement de la base nettoyée...")

df = pd.read_csv(
    DATA_FILE,
    sep=";"
)

print(f"Nombre de lignes : {len(df):,}")
print(f"Nombre de colonnes : {len(df.columns)}")


# ============================================================
# 1. Doublons SIRET
# ============================================================

print("\n" + "=" * 60)
print("1. DOUBLONS SIRET")
print("=" * 60)

doublons_siret = df["siret"].duplicated().sum()

print(f"Nombre de SIRET dupliqués : {doublons_siret}")

if doublons_siret == 0:
    print("OK : aucun doublon SIRET.")
else:
    print("ATTENTION : des doublons SIRET sont présents.")


# ============================================================
# 2. Valeurs manquantes
# ============================================================

print("\n" + "=" * 60)
print("2. VALEURS MANQUANTES")
print("=" * 60)

missing = (
    df.isna()
    .sum()
    .sort_values(ascending=False)
)

missing_percent = (
    df.isna()
    .mean()
    .mul(100)
    .sort_values(ascending=False)
)

missing_table = pd.DataFrame({
    "nombre": missing,
    "pourcentage": missing_percent.round(2)
})

print(missing_table)


# ============================================================
# 3. Coordonnées géographiques
# ============================================================

print("\n" + "=" * 60)
print("3. COORDONNÉES GÉOGRAPHIQUES")
print("=" * 60)

missing_latitude = df["latitude"].isna().sum()
missing_longitude = df["longitude"].isna().sum()

print(f"Latitude manquante : {missing_latitude}")
print(f"Longitude manquante : {missing_longitude}")

print("\nStatistiques latitude :")
print(df["latitude"].describe())

print("\nStatistiques longitude :")
print(df["longitude"].describe())


# ============================================================
# 4. Vérification des coordonnées aberrantes
# ============================================================

print("\n" + "=" * 60)
print("4. COORDONNÉES ABERRANTES")
print("=" * 60)

coord_aberrantes = df[
    (df["latitude"].notna())
    & (
        (df["latitude"] < 46)
        | (df["latitude"] > 48)
        | (df["longitude"] < -2.5)
        | (df["longitude"] > 0)
    )
]

print(
    f"Nombre de coordonnées potentiellement aberrantes : "
    f"{len(coord_aberrantes)}"
)

if len(coord_aberrantes) > 0:
    print("\nExemples :")
    print(
        coord_aberrantes[
            [
                "siret",
                "commune",
                "latitude",
                "longitude"
            ]
        ].head(10)
    )


# ============================================================
# 5. Dates de création
# ============================================================

print("\n" + "=" * 60)
print("5. DATES DE CRÉATION")
print("=" * 60)

df["date_creation"] = pd.to_datetime(
    df["date_creation"],
    errors="coerce"
)

print("Date de création la plus ancienne :")
print(df["date_creation"].min())

print("\nDate de création la plus récente :")
print(df["date_creation"].max())

print("\nDates de création dans le futur :")

dates_futures = df[
    df["date_creation"] > pd.Timestamp.today()
]

print(len(dates_futures))


# ============================================================
# 6. Dates de fermeture
# ============================================================

print("\n" + "=" * 60)
print("6. DATES DE FERMETURE")
print("=" * 60)

df["date_fermeture"] = pd.to_datetime(
    df["date_fermeture"],
    errors="coerce"
)

print("Date de fermeture la plus ancienne :")
print(df["date_fermeture"].min())

print("\nDate de fermeture la plus récente :")
print(df["date_fermeture"].max())

print("\nFermetures avant création :")

fermeture_avant_creation = df[
    (df["date_creation"].notna())
    & (df["date_fermeture"].notna())
    & (df["date_fermeture"] < df["date_creation"])
]

print(len(fermeture_avant_creation))


# ============================================================
# 7. Cohérence du statut
# ============================================================

print("\n" + "=" * 60)
print("7. STATUT ADMINISTRATIF")
print("=" * 60)

print(df["statut"].value_counts(dropna=False))

print("\nÉtablissements actifs avec une date de fermeture :")

actifs_fermes = df[
    (df["statut"] == "Actif")
    & (df["date_fermeture"].notna())
]

print(len(actifs_fermes))

print("\nÉtablissements fermés sans date de fermeture :")

fermes_sans_date = df[
    (df["statut"] == "Fermé")
    & (df["date_fermeture"].isna())
]

print(len(fermes_sans_date))


# ============================================================
# 8. Contrôle des codes NAF
# ============================================================

print("\n" + "=" * 60)
print("8. CODES NAF")
print("=" * 60)

codes_attendus = {
    "56.10A",
    "56.10B",
    "56.10C",
    "56.30Z",
}

codes_observes = set(
    df["code_naf"].dropna().unique()
)

print("Codes observés :", sorted(codes_observes))
print("Codes attendus :", sorted(codes_attendus))

codes_inattendus = codes_observes - codes_attendus

print(
    f"Codes inattendus : {codes_inattendus}"
)


# ============================================================
# 9. Résumé final
# ============================================================

print("\n" + "=" * 60)
print("9. RÉSUMÉ DU CONTRÔLE")
print("=" * 60)

print(f"Lignes : {len(df):,}")
print(f"Colonnes : {len(df.columns)}")
print(f"Doublons SIRET : {doublons_siret}")
print(f"Dates de création futures : {len(dates_futures)}")
print(
    f"Fermetures avant création : "
    f"{len(fermeture_avant_creation)}"
)
print(
    f"Actifs avec date de fermeture : "
    f"{len(actifs_fermes)}"
)
print(
    f"Fermés sans date de fermeture : "
    f"{len(fermes_sans_date)}"
)
print(
    f"Coordonnées potentiellement aberrantes : "
    f"{len(coord_aberrantes)}"
)

print("\nContrôle qualité terminé.")