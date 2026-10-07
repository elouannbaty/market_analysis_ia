from pathlib import Path
import pandas as pd


PROJECT_DIR = Path(__file__).resolve().parents[2]

PROCESSED_DIR = PROJECT_DIR / "data" / "processed"
EXTERNAL_DIR = PROJECT_DIR / "data" / "external"

SIRENE_FILE = PROCESSED_DIR / "table_analytique_restauration.csv"
INSEE_FILE = EXTERNAL_DIR / "comparateur.csv"

OUTPUT_FILE = EXTERNAL_DIR / "donnees_territoriales_insee.csv"


def construire_donnees_territoriales():

    print("Chargement des données...")

    sirene = pd.read_csv(
        SIRENE_FILE,
        sep=";",
        low_memory=False
    )

    insee = pd.read_csv(
        INSEE_FILE,
        sep=";",
        low_memory=False
    )

    # ---------------------------------------------------------------
    # 1. Récupération des communes du périmètre
    # ---------------------------------------------------------------

    communes = (
    sirene[
        ["code_commune", "commune"]
    ]
    .sort_values("code_commune")
    .drop_duplicates(
        subset="code_commune",
        keep="first"
    )
)

    # Harmonisation des codes communes
    communes["code_commune"] = (
        communes["code_commune"]
        .astype(str)
        .str.zfill(5)
    )

    print(
        "\nNombre de communes dans SIRENE :",
        len(communes)
    )

    # ---------------------------------------------------------------
    # 2. Filtrage des données Insee au niveau communal
    # ---------------------------------------------------------------

    insee = insee[
        insee["GEO_OBJECT"] == "COM"
    ].copy()

    # Harmonisation des codes communes Insee
    insee["GEO"] = (
        insee["GEO"]
        .astype(str)
        .str.zfill(5)
    )

    # ---------------------------------------------------------------
    # 3. Population 2017
    # ---------------------------------------------------------------

    population_2017 = (
        insee[
            (insee["TAB_MEASURE"] == "POP")
            & (insee["TIME_PERIOD"] == 2017)
        ][
            ["GEO", "OBS_VALUE"]
        ]
        .rename(
            columns={
                "GEO": "code_commune",
                "OBS_VALUE": "population_2017"
            }
        )
    )

    # ---------------------------------------------------------------
    # 4. Population 2023
    # ---------------------------------------------------------------

    population_2023 = (
        insee[
            (insee["TAB_MEASURE"] == "POP")
            & (insee["TIME_PERIOD"] == 2023)
        ][
            ["GEO", "OBS_VALUE"]
        ]
        .rename(
            columns={
                "GEO": "code_commune",
                "OBS_VALUE": "population_2023"
            }
        )
    )

    # ---------------------------------------------------------------
    # 5. Superficie 2023
    # ---------------------------------------------------------------

    superficie = (
        insee[
            (insee["TAB_MEASURE"] == "SUP")
            & (insee["TIME_PERIOD"] == 2023)
        ][
            ["GEO", "OBS_VALUE"]
        ]
        .rename(
            columns={
                "GEO": "code_commune",
                "OBS_VALUE": "superficie_km2"
            }
        )
    )

    # ---------------------------------------------------------------
    # 6. Niveau de vie médian 2023
    # ---------------------------------------------------------------

    niveau_vie = (
        insee[
            (insee["TAB_MEASURE"] == "MED_SL")
            & (insee["TIME_PERIOD"] == 2023)
        ][
            ["GEO", "OBS_VALUE"]
        ]
        .rename(
            columns={
                "GEO": "code_commune",
                "OBS_VALUE": "niveau_vie_median"
            }
        )
    )

    # ---------------------------------------------------------------
    # 7. Fusion des données
    # ---------------------------------------------------------------

    resultats = communes.copy()

    for donnees in [
        population_2017,
        population_2023,
        superficie,
        niveau_vie
    ]:
        resultats = resultats.merge(
            donnees,
            on="code_commune",
            how="left"
        )

    # ---------------------------------------------------------------
    # 8. Conversion numérique
    # ---------------------------------------------------------------

    colonnes_numeriques = [
        "population_2017",
        "population_2023",
        "superficie_km2",
        "niveau_vie_median"
    ]

    for colonne in colonnes_numeriques:
        resultats[colonne] = pd.to_numeric(
            resultats[colonne],
            errors="coerce"
        )

    # ---------------------------------------------------------------
    # 9. Calcul de la densité
    # ---------------------------------------------------------------

    resultats["densite_2023"] = (
        resultats["population_2023"]
        / resultats["superficie_km2"]
    )

    # ---------------------------------------------------------------
    # 10. Variation annuelle moyenne de population
    # ---------------------------------------------------------------

    resultats["variation_population_annuelle"] = (
        (
            resultats["population_2023"]
            / resultats["population_2017"]
        ) ** (1 / 6)
        - 1
    ) * 100

    # ---------------------------------------------------------------
    # 11. Arrondi
    # ---------------------------------------------------------------

    resultats["densite_2023"] = resultats[
        "densite_2023"
    ].round(1)

    resultats["variation_population_annuelle"] = resultats[
        "variation_population_annuelle"
    ].round(2)

    # ---------------------------------------------------------------
    # 12. Contrôles
    # ---------------------------------------------------------------

    print("\n" + "=" * 70)
    print("CONTRÔLES")
    print("=" * 70)

    print(
        "Nombre de communes finales :",
        len(resultats)
    )

    print(
        "Communes sans population 2023 :",
        resultats["population_2023"].isna().sum()
    )

    print(
        "Communes sans superficie :",
        resultats["superficie_km2"].isna().sum()
    )

    print(
        "Communes sans niveau de vie :",
        resultats["niveau_vie_median"].isna().sum()
    )

    print("\n" + "=" * 70)
    print("APERÇU")
    print("=" * 70)

    print(
        resultats.to_string(index=False)
    )

    # ---------------------------------------------------------------
    # 13. Sauvegarde
    # ---------------------------------------------------------------

    resultats.to_csv(
        OUTPUT_FILE,
        sep=";",
        index=False
    )

    print("\n" + "=" * 70)
    print("SAUVEGARDE")
    print("=" * 70)

    print("Fichier créé :")
    print(OUTPUT_FILE)


if __name__ == "__main__":
    construire_donnees_territoriales()