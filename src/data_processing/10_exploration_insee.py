from pathlib import Path
import pandas as pd


PROJECT_DIR = Path(__file__).resolve().parents[2]

DATA_FILE = (
    PROJECT_DIR
    / "data"
    / "external"
    / "comparateur.csv"
)


def explorer_insee():

    print("Chargement de la base Insee...")

    df = pd.read_csv(
        DATA_FILE,
        sep=";",
        low_memory=False
    )

    # On travaille uniquement sur les communes
    communes = df[df["GEO_OBJECT"] == "COM"].copy()

    print("\n" + "=" * 70)
    print("DONNÉES COMMUNALES")
    print("=" * 70)

    print(f"Nombre de lignes communales : {len(communes):,}")
    print(f"Nombre de communes distinctes : {communes['GEO'].nunique():,}")

    print("\n" + "=" * 70)
    print("MESURES POUR LES COMMUNES")
    print("=" * 70)

    mesures = (
        communes[
            [
                "TAB_MEASURE",
                "TIME_PERIOD"
            ]
        ]
        .drop_duplicates()
        .sort_values(
            ["TAB_MEASURE", "TIME_PERIOD"]
        )
    )

    print(mesures.to_string(index=False))


if __name__ == "__main__":
    explorer_insee()