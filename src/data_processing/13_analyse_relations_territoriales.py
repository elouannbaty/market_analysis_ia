from pathlib import Path
import pandas as pd


PROJECT_DIR = Path(__file__).resolve().parents[2]

PROCESSED_DIR = PROJECT_DIR / "data" / "processed"

INPUT_FILE = PROCESSED_DIR / "marche_restauration_territoire.csv"
OUTPUT_FILE = PROCESSED_DIR / "correlations_territoriales.csv"


def analyser_relations_territoriales():

    print("Chargement des données...")

    df = pd.read_csv(
        INPUT_FILE,
        sep=";"
    )

    # ---------------------------------------------------------------
    # 1. Variables étudiées
    # ---------------------------------------------------------------

    variables = [
        "etablissements_total",
        "etablissements_actifs",
        "taux_fermeture",
        "restaurants",
        "restauration_rapide",
        "cafes_bars",
        "population_2023",
        "densite_2023",
        "variation_population_annuelle",
        "niveau_vie_median",
        "etablissements_pour_1000_habitants",
        "actifs_pour_1000_habitants"
    ]

    donnees = df[variables].copy()

    # ---------------------------------------------------------------
    # 2. Matrice de corrélation
    # ---------------------------------------------------------------

    correlations = donnees.corr(
        method="pearson"
    )

    # ---------------------------------------------------------------
    # 3. Sauvegarde
    # ---------------------------------------------------------------

    correlations.to_csv(
        OUTPUT_FILE,
        sep=";"
    )

    # ---------------------------------------------------------------
    # 4. Contrôles
    # ---------------------------------------------------------------

    print("\n" + "=" * 70)
    print("CONTRÔLES")
    print("=" * 70)

    print(
        "Nombre de communes :",
        len(df)
    )

    print(
        "Nombre de variables :",
        len(variables)
    )

    print(
        "Valeurs manquantes :",
        donnees.isna().sum().sum()
    )

    # ---------------------------------------------------------------
    # 5. Relations avec le nombre d'établissements
    # ---------------------------------------------------------------

    print("\n" + "=" * 70)
    print("CORRÉLATIONS AVEC LE NOMBRE TOTAL D'ÉTABLISSEMENTS")
    print("=" * 70)

    correlations_total = (
        correlations["etablissements_total"]
        .drop("etablissements_total")
        .sort_values(
            key=lambda x: x.abs(),
            ascending=False
        )
    )

    print(
        correlations_total.to_string()
    )

    # ---------------------------------------------------------------
    # 6. Relations avec la densité d'établissements
    # ---------------------------------------------------------------

    print("\n" + "=" * 70)
    print("CORRÉLATIONS AVEC LES ÉTABLISSEMENTS POUR 1 000 HABITANTS")
    print("=" * 70)

    correlations_densite = (
        correlations["etablissements_pour_1000_habitants"]
        .drop("etablissements_pour_1000_habitants")
        .sort_values(
            key=lambda x: x.abs(),
            ascending=False
        )
    )

    print(
        correlations_densite.to_string()
    )

    # ---------------------------------------------------------------
    # 7. Relations avec le taux historique de fermeture
    # ---------------------------------------------------------------

    print("\n" + "=" * 70)
    print("CORRÉLATIONS AVEC LE TAUX HISTORIQUE DE FERMETURE")
    print("=" * 70)

    correlations_fermeture = (
        correlations["taux_fermeture"]
        .drop("taux_fermeture")
        .sort_values(
            key=lambda x: x.abs(),
            ascending=False
        )
    )

    print(
        correlations_fermeture.to_string()
    )

    # ---------------------------------------------------------------
    # 8. Sauvegarde
    # ---------------------------------------------------------------

    print("\n" + "=" * 70)
    print("SAUVEGARDE")
    print("=" * 70)

    print("Fichier créé :")
    print(OUTPUT_FILE)


if __name__ == "__main__":
    analyser_relations_territoriales()