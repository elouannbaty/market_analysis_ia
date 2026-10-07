from pathlib import Path
import requests


DATASET_ID = "244400404_base-sirene-entreprises-nantes-metropole"

URL = (
    "https://data.nantesmetropole.fr/api/explore/v2.1/"
    f"catalog/datasets/{DATASET_ID}/exports/csv"
)

OUTPUT_DIR = Path(__file__).resolve().parents[2] / "data" / "raw"
OUTPUT_FILE = OUTPUT_DIR / "sirene_nantes_metropole.csv"


def download_sirene():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    print("Téléchargement de la base SIRENE...")

    response = requests.get(URL, timeout=120)
    response.raise_for_status()

    OUTPUT_FILE.write_bytes(response.content)

    print("Téléchargement terminé.")
    print(f"Fichier créé : {OUTPUT_FILE}")


if __name__ == "__main__":
    download_sirene()