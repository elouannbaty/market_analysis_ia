from pathlib import Path
import pandas as pd


PROJECT_DIR = Path(__file__).resolve().parents[2]

PROCESSED_DIR = PROJECT_DIR / "data" / "processed"

INPUT_FILE = PROCESSED_DIR / "marche_restauration_territoire.csv"
OUTPUT_FILE = PROCESSED_DIR / "profils_territoriaux.csv"


def construire_profils():

    print("Chargement des données...")

    df = pd.read_csv(
        INPUT_FILE,
        sep=";"
    )

    # ---------------------------------------------------------------
    # 1. Médianes du territoire
    # ---------------------------------------------------------------

    mediane_densite = df["densite_2023"].median()

    mediane_offre = df[
        "etablissements_pour_1000_habitants"
    ].median()

    mediane_niveau_vie = df[
        "niveau_vie_median"
    ].median()

    print("\n" + "=" * 70)
    print("MÉDIANES")
    print("=" * 70)

    print(
        "Densité médiane :",
        round(mediane_densite, 1)
    )

    print(
        "Établissements pour 1 000 habitants - médiane :",
        round(mediane_offre, 2)
    )

    print(
        "Niveau de vie médian du territoire :",
        round(mediane_niveau_vie, 0)
    )

    # ---------------------------------------------------------------
    # 2. Intensité de l'offre
    # ---------------------------------------------------------------

    df["intensite_offre"] = (
        df["etablissements_pour_1000_habitants"]
        >= mediane_offre
    )

    # ---------------------------------------------------------------
    # 3. Densité du territoire
    # ---------------------------------------------------------------

    df["territoire_dense"] = (
        df["densite_2023"]
        >= mediane_densite
    )

    # ---------------------------------------------------------------
    # 4. Profil territorial
    # ---------------------------------------------------------------

    def definir_profil(row):

        if row["territoire_dense"] and row["intensite_offre"]:
            return "Dense / offre forte"

        if row["territoire_dense"] and not row["intensite_offre"]:
            return "Dense / offre faible"

        if not row["territoire_dense"] and row["intensite_offre"]:
            return "Peu dense / offre forte"

        return "Peu dense / offre faible"

    df["profil_territorial"] = df.apply(
        definir_profil,
        axis=1
    )

    # ---------------------------------------------------------------
    # 5. Écart à la médiane de l'offre
    # ---------------------------------------------------------------

    df["ecart_offre_vs_mediane_pct"] = (
        (
            df["etablissements_pour_1000_habitants"]
            / mediane_offre
        ) - 1
    ) * 100

    df["ecart_offre_vs_mediane_pct"] = (
        df["ecart_offre_vs_mediane_pct"]
        .round(1)
    )

    # ---------------------------------------------------------------
    # 6. Écart à la médiane de densité
    # ---------------------------------------------------------------

    df["ecart_densite_vs_mediane_pct"] = (
        (
            df["densite_2023"]
            / mediane_densite
        ) - 1
    ) * 100

    df["ecart_densite_vs_mediane_pct"] = (
        df["ecart_densite_vs_mediane_pct"]
        .round(1)
    )

    # ---------------------------------------------------------------
    # 7. Classement de l'offre
    # ---------------------------------------------------------------

    df["rang_offre_1000_habitants"] = (
        df["etablissements_pour_1000_habitants"]
        .rank(
            ascending=False,
            method="min"
        )
        .astype(int)
    )

    # ---------------------------------------------------------------
    # 8. Classement du niveau de vie
    # ---------------------------------------------------------------

    df["rang_niveau_vie"] = (
        df["niveau_vie_median"]
        .rank(
            ascending=False,
            method="min"
        )
        .astype(int)
    )

    # ---------------------------------------------------------------
    # 9. Tri
    # ---------------------------------------------------------------

    df = df.sort_values(
        "rang_offre_1000_habitants"
    )

    # ---------------------------------------------------------------
    # 10. Contrôles
    # ---------------------------------------------------------------

    print("\n" + "=" * 70)
    print("RÉPARTITION DES PROFILS")
    print("=" * 70)

    print(
        df["profil_territorial"]
        .value_counts()
        .to_string()
    )

    print("\n" + "=" * 70)
    print("CLASSEMENT DE L'OFFRE")
    print("=" * 70)

    print(
        df[
            [
                "commune",
                "etablissements_pour_1000_habitants",
                "densite_2023",
                "niveau_vie_median",
                "profil_territorial",
                "rang_offre_1000_habitants"
            ]
        ]
        .to_string(index=False)
    )

    # ---------------------------------------------------------------
    # 11. Sauvegarde
    # ---------------------------------------------------------------

    df.to_csv(
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
    construire_profils()