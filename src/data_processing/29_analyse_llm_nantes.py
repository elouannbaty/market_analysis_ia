from pathlib import Path
import requests


BASE_DIR = Path(__file__).resolve().parents[2]

FICHIER_PROMPT = BASE_DIR / "docs" / "prompt_llm_v0.md"
FICHIER_CONTEXTE = BASE_DIR / "data" / "processed" / "contexte_ia_nantes.json"

FICHIER_SORTIE = BASE_DIR / "data" / "processed" / "analyse_llm_nantes.md"

URL_OLLAMA = "http://localhost:11434/api/generate"


# Vérification des fichiers nécessaires
if not FICHIER_PROMPT.exists():
    raise FileNotFoundError(
        f"Prompt introuvable : {FICHIER_PROMPT}"
    )

if not FICHIER_CONTEXTE.exists():
    raise FileNotFoundError(
        f"Contexte introuvable : {FICHIER_CONTEXTE}"
    )


# Lecture du prompt
prompt_systeme = FICHIER_PROMPT.read_text(
    encoding="utf-8"
)

# Lecture du contexte de données
contexte_json = FICHIER_CONTEXTE.read_text(
    encoding="utf-8"
)


# Construction de la demande
prompt = (
    prompt_systeme
    + "\n\n"
    + "---\n\n"
    + "# CONTEXTE DE DONNÉES\n\n"
    + contexte_json
    + "\n\n"
    + "---\n\n"
    + "Produis maintenant l'analyse de Nantes "
      "en respectant strictement toutes les règles "
      "définies dans le prompt."
)


payload = {
    "model": "qwen3:8b",
    "prompt": prompt,
    "stream": False
}


print("=" * 70)
print("ANALYSE MARKET INTELLIGENCE — NANTES")
print("=" * 70)
print("Envoi de la demande à Qwen3...")
print()


# Appel à Ollama
response = requests.post(
    URL_OLLAMA,
    json=payload
)

response.raise_for_status()

resultat = response.json()["response"]


# Affichage dans le terminal
print(resultat)


# Sauvegarde de l'analyse
FICHIER_SORTIE.write_text(
    resultat,
    encoding="utf-8"
)


print()
print("=" * 70)
print("ANALYSE TERMINÉE")
print("=" * 70)
print(f"Analyse sauvegardée dans :")
print(FICHIER_SORTIE)
print("=" * 70)