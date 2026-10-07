from pathlib import Path
import pandas as pd


PROJECT_DIR = Path(__file__).resolve().parents[2]

PROCESSED_DIR = PROJECT_DIR / "data" / "processed"
EXTERNAL_DIR = PROJECT_DIR / "data" / "external"

SIRENE_FILE = PROCESSED_DIR / "table_analytique_restauration.csv"
INSEE_FILE = EXTERNAL_DIR / "donnees_territoriales_insee.csv"

OUTPUT_FILE = PROCESSED_DIR / "marche_restauration_territoire.csv"


def construire_croisement():

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
    # 1. Harmonisation des codes communes
    # ---------------------------------------------------------------

    sirene["code_commune"] = (
        sirene["code_commune"]
        .astype(str)
        .str.zfill(5)
    )

    insee["code_commune"] = (
        insee["code_commune"]
        .astype(str)
        .str.zfill(5)
    )

    # ---------------------------------------------------------------
    # 2. Agrégation du marché de la restauration
    # ---------------------------------------------------------------

    marche = (
        sirene
        .groupby("code_commune")
        .agg(
            commune=("commune", "first"),
            etablissements_total=("siret", "count"),
            etablissements_actifs=("est_ferme", lambda x: (~x).sum()),
            etablissements_fermes=("est_ferme", "sum"),
            entreprises=("siren", "nunique"),
        )
        .reset_index()
    )

    # ---------------------------------------------------------------
    # 3. Répartition par catégorie
    # ---------------------------------------------------------------

    categories = pd.crosstab(
        sirene["code_commune"],
        sirene["categorie"]
    )

    categories = categories.reset_index()

    categories = categories.rename(
        columns={
            "Restaurant": "restaurants",
            "Restauration rapide": "restauration_rapide",
            "Café et bar": "cafes_bars"
        }
    )

    # ---------------------------------------------------------------
    # 4. Fusion avec les données du marché
    # ---------------------------------------------------------------

    marche = marche.merge(
        categories,
        on="code_commune",
        how="left"
    )

    # ---------------------------------------------------------------
    # 5. Fusion avec les données Insee
    # ---------------------------------------------------------------

    resultats = marche.merge(
        insee,
        on="code_commune",
        how="left",
        suffixes=("", "_insee")
    )

    # ---------------------------------------------------------------
    # 6. Calcul du taux historique de fermeture
    # ---------------------------------------------------------------

    resultats["taux_fermeture"] = (
        resultats["etablissements_fermes"]
        / resultats["etablissements_total"]
        * 100
    )

    # ---------------------------------------------------------------
    # 7. Nombre d'établissements pour 1 000 habitants
    # ---------------------------------------------------------------

    resultats["etablissements_pour_1000_habitants"] = (
        resultats["etablissements_total"]
        / resultats["population_2023"]
        * 1000
    )

    # ---------------------------------------------------------------
    # 8. Nombre d'établissements actifs pour 1 000 habitants
    # ---------------------------------------------------------------

    resultats["actifs_pour_1000_habitants"] = (
        resultats["etablissements_actifs"]
        / resultats["population_2023"]
        * 1000
    )

    # ---------------------------------------------------------------
    # 9. Arrondis
    # ---------------------------------------------------------------

    resultats["taux_fermeture"] = (
        resultats["taux_fermeture"].round(2)
    )

    resultats["etablissements_pour_1000_habitants"] = (
        resultats["etablissements_pour_1000_habitants"].round(2)
    )

    resultats["actifs_pour_1000_habitants"] = (
        resultats["actifs_pour_1000_habitants"].round(2)
    )

    # ---------------------------------------------------------------
    # 10. Sélection des colonnes
    # ---------------------------------------------------------------

    colonnes = [
        "code_commune",
        "commune",
        "etablissements_total",
        "etablissements_actifs",
        "etablissements_fermes",
        "taux_fermeture",
        "entreprises",
        "restaurants",
        "restauration_rapide",
        "cafes_bars",
        "population_2017",
        "population_2023",
        "superficie_km2",
        "densite_2023",
        "variation_population_annuelle",
        "niveau_vie_median",
        "etablissements_pour_1000_habitants",
        "actifs_pour_1000_habitants"
    ]

    resultats = resultats[colonnes]

    # ---------------------------------------------------------------
    # 11. Tri
    # ---------------------------------------------------------------

    resultats = resultats.sort_values(
        "etablissements_total",
        ascending=False
    )

    # ---------------------------------------------------------------
    # 12. Contrôles
    # ---------------------------------------------------------------

    print("\n" + "=" * 70)
    print("CONTRÔLES")
    print("=" * 70)

    print(
        "Nombre de communes :",
        len(resultats)
    )

    print(
        "Colonnes :",
        len(resultats.columns)
    )

    print(
        "Communes sans données Insee :",
        resultats["population_2023"].isna().sum()
    )

    print(
        "Doublons de codes communes :",
        resultats["code_commune"].duplicated().sum()
    )

    print(
        "Valeurs manquantes niveau de vie :",
        resultats["niveau_vie_median"].isna().sum()
    )

    print("\n" + "=" * 70)
    print("TOP 10 COMMUNES")
    print("=" * 70)

    print(
        resultats[
            [
                "commune",
                "etablissements_total",
                "etablissements_actifs",
                "taux_fermeture",
                "population_2023",
                "densite_2023",
                "niveau_vie_median"
            ]
        ]
        .head(10)
        .to_string(index=False)
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
    construire_croisement()