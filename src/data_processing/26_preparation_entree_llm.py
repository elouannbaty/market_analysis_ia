from pathlib import Path


# ============================================================
# 1. CHEMINS
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[2]

FICHIER_PROMPT = (
    BASE_DIR
    / "docs"
    / "prompt_llm_v0.md"
)

FICHIER_CONTEXTE = (
    BASE_DIR
    / "data"
    / "processed"
    / "contexte_ia_nantes.json"
)


# ============================================================
# 2. VÉRIFICATION DES FICHIERS
# ============================================================

if not FICHIER_PROMPT.exists():
    raise FileNotFoundError(
        f"Prompt introuvable : {FICHIER_PROMPT}"
    )

if not FICHIER_CONTEXTE.exists():
    raise FileNotFoundError(
        f"Contexte introuvable : {FICHIER_CONTEXTE}"
    )


# ============================================================
# 3. LECTURE DES FICHIERS
# ============================================================

prompt_systeme = FICHIER_PROMPT.read_text(
    encoding="utf-8"
)

contexte_json = FICHIER_CONTEXTE.read_text(
    encoding="utf-8"
)


# ============================================================
# 4. CONSTRUCTION DE L'ENTRÉE LLM
# ============================================================

entree_llm = (
    prompt_systeme
    + "\n\n"
    + "---\n\n"
    + "# CONTEXTE DE DONNÉES\n\n"
    + "Voici le contexte structuré fourni par le système.\n\n"
    + contexte_json
    + "\n\n"
    + "---\n\n"
    + "À partir de ce contexte, produis une analyse de "
      "Market Intelligence en respectant strictement les "
      "règles définies précédemment.\n"
)


# ============================================================
# 5. AFFICHAGE
# ============================================================

print("=" * 70)
print("ENTRÉE LLM — TEST")
print("=" * 70)

print(entree_llm)

print("=" * 70)
print("Vérification terminée.")
print("=" * 70)