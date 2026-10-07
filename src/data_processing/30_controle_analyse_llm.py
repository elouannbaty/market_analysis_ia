from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[2]

FICHIER_ANALYSE = (
    BASE_DIR
    / "data"
    / "processed"
    / "analyse_llm_nantes.md"
)


if not FICHIER_ANALYSE.exists():
    raise FileNotFoundError(
        f"Analyse introuvable : {FICHIER_ANALYSE}"
    )


analyse = FICHIER_ANALYSE.read_text(
    encoding="utf-8"
)

# Normalisation des espaces Unicode
analyse_controle = " ".join(analyse.split())


print("=" * 70)
print("CONTRÔLE DE L'ANALYSE LLM")
print("=" * 70)


# --------------------------------------------------
# 1. Vérification des sections obligatoires
# --------------------------------------------------

sections_obligatoires = [
    "## 1. Vue d'ensemble",
    "## 2. Dynamique du marché",
    "## 3. Segments",
    "## 4. Structure concurrentielle",
    "## 5. Signaux",
    "## 6. Synthèse",
    "## 7. Limites",
]


sections_manquantes = [
    section
    for section in sections_obligatoires
    if section not in analyse_controle
]


if sections_manquantes:
    print("❌ Sections manquantes :")
    for section in sections_manquantes:
        print(f"   - {section}")
else:
    print("✅ Toutes les sections obligatoires sont présentes.")


# --------------------------------------------------
# 2. Recherche de formulations interdites
# --------------------------------------------------

formulations_interdites = [
    "marché saturé",
    "marché sursaturé",
    "forte saturation",
    "forte concurrence",
    "concurrence intense",
    "pression concurrentielle élevée",
]


formulations_detectees = [
    formulation
    for formulation in formulations_interdites
    if formulation.lower() in analyse.lower()
]


if formulations_detectees:
    print("❌ Formulations problématiques détectées :")
    for formulation in formulations_detectees:
        print(f"   - {formulation}")
else:
    print("✅ Aucune formulation problématique détectée.")


# --------------------------------------------------
# 3. Vérification des principaux indicateurs
# --------------------------------------------------

elements_attendus = [
    ["5350", "5 350", "5\u00a0350"],
    ["1782", "1 782", "1\u00a0782"],
    ["66,69", "66.69"],
    ["776"],
    ["709"],
    ["+67"],
    ["6,1", "6.1"],
    ["1,01", "1.01"],
    ["1,68", "1.68"],
]


elements_manquants = []

for variantes in elements_attendus:
    if not any(
        variante in analyse_controle
        for variante in variantes
    ):
        elements_manquants.append(variantes[0])


if elements_manquants:
    print("❌ Indicateurs attendus absents :")
    for element in elements_manquants:
        print(f"   - {element}")
else:
    print("✅ Les principaux indicateurs attendus sont présents.")


# --------------------------------------------------
# 4. Résultat global
# --------------------------------------------------

controle_ok = (
    not sections_manquantes
    and not formulations_detectees
    and not elements_manquants
)


print()
print("=" * 70)

if controle_ok:
    print("✅ CONTRÔLE RÉUSSI")
else:
    print("❌ CONTRÔLE ÉCHOUÉ")

print("=" * 70)