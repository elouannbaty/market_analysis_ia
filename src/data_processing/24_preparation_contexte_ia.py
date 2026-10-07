from pathlib import Path
import json

import pandas as pd


# ============================================================
# 1. PARAMÈTRES
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[2]

FICHIER_PROFILS = (
    BASE_DIR
    / "data"
    / "processed"
    / "profils_qualitatifs_communes.csv"
)

FICHIER_MARCHE = (
    BASE_DIR
    / "data"
    / "processed"
    / "marche_restauration_territoire.csv"
)

FICHIER_DYNAMIQUE = (
    BASE_DIR
    / "data"
    / "processed"
    / "dynamique_restauration_categorie.csv"
)

FICHIER_SORTIE = (
    BASE_DIR
    / "data"
    / "processed"
    / "contexte_ia_nantes.json"
)


# ============================================================
# 2. CHARGEMENT DES DONNÉES
# ============================================================

profils = pd.read_csv(
    FICHIER_PROFILS,
    sep=";",
    low_memory=False
)

marche = pd.read_csv(
    FICHIER_MARCHE,
    sep=";",
    low_memory=False
)

dynamique = pd.read_csv(
    FICHIER_DYNAMIQUE,
    sep=";",
    low_memory=False
)


# ============================================================
# 3. SÉLECTION DE NANTES
# ============================================================

profil_nantes = profils[
    profils["commune"] == "NANTES"
]

marche_nantes = marche[
    marche["commune"] == "NANTES"
]

dynamique_nantes = dynamique[
    dynamique["commune"] == "NANTES"
]


if profil_nantes.empty:
    raise ValueError(
        "NANTES n'a pas été trouvée dans "
        "profils_qualitatifs_communes.csv"
    )

if marche_nantes.empty:
    raise ValueError(
        "NANTES n'a pas été trouvée dans "
        "marche_restauration_territoire.csv"
    )

if dynamique_nantes.empty:
    raise ValueError(
        "NANTES n'a pas été trouvée dans "
        "dynamique_restauration_categorie.csv"
    )


profil_nantes = profil_nantes.iloc[0]
marche_nantes = marche_nantes.iloc[0]
dynamique_nantes = dynamique_nantes.iloc[0]


# ============================================================
# 4. FONCTION DE CONVERSION
# ============================================================

def valeur(valeur_entree):
    """
    Convertit les valeurs pandas / NumPy
    en types compatibles avec JSON.
    """

    if pd.isna(valeur_entree):
        return None

    if hasattr(valeur_entree, "item"):
        return valeur_entree.item()

    return valeur_entree


# ============================================================
# 5. CONSTRUCTION DU CONTEXTE
# ============================================================

contexte = {

    # --------------------------------------------------------
    # COMMUNE
    # --------------------------------------------------------

    "commune": "NANTES",


    # --------------------------------------------------------
    # MARCHÉ
    # --------------------------------------------------------

    "marche": {

        "etablissements_total": valeur(
            profil_nantes["etablissements_total"]
        ),

        "etablissements_actifs": valeur(
            profil_nantes["etablissements_actifs"]
        ),

        "etablissements_fermes": valeur(
            profil_nantes["etablissements_fermes"]
        ),

        "entreprises": valeur(
            profil_nantes["entreprises"]
        ),

        "etablissements_pour_1000_habitants": valeur(
            profil_nantes[
                "etablissements_pour_1000_habitants"
            ]
        ),

        "actifs_pour_1000_habitants": valeur(
            profil_nantes[
                "actifs_pour_1000_habitants"
            ]
        ),

        "taux_fermeture_historique": valeur(
            profil_nantes["taux_fermeture"]
        )
    },


    # --------------------------------------------------------
    # TERRITOIRE
    # --------------------------------------------------------

    "territoire": {

        "population_2023": valeur(
            profil_nantes["population_2023"]
        ),

        "densite_2023": valeur(
            marche_nantes["densite_2023"]
        ),

        "niveau_vie_median": valeur(
            profil_nantes["niveau_vie_median"]
        )
    },


    # --------------------------------------------------------
    # DYNAMIQUE GLOBALE
    # --------------------------------------------------------

    "dynamique": {

        "periode": "2022-2025",

        "creations": valeur(
            profil_nantes["creations_2022_2025"]
        ),

        "fermetures": valeur(
            profil_nantes["fermetures_2022_2025"]
        ),

        "solde": valeur(
            profil_nantes["solde_2022_2025"]
        ),

        "solde_pour_1000_habitants": valeur(
            profil_nantes["solde_pour_1000_hab"]
        )
    },


    # --------------------------------------------------------
    # CATÉGORIES
    # --------------------------------------------------------

    "categories": {

        "restaurant": {

            "creations": valeur(
                dynamique_nantes[
                    "restaurants_creations"
                ]
            ),

            "fermetures": valeur(
                dynamique_nantes[
                    "restaurants_fermetures"
                ]
            ),

            "solde": valeur(
                dynamique_nantes[
                    "restaurants_solde"
                ]
            ),

            "solde_pour_1000_habitants": valeur(
                dynamique_nantes[
                    "restaurants_solde_pour_1000"
                ]
            )
        },


        "restauration_rapide": {

            "creations": valeur(
                dynamique_nantes[
                    "rapide_creations"
                ]
            ),

            "fermetures": valeur(
                dynamique_nantes[
                    "rapide_fermetures"
                ]
            ),

            "solde": valeur(
                dynamique_nantes[
                    "rapide_solde"
                ]
            ),

            "solde_pour_1000_habitants": valeur(
                dynamique_nantes[
                    "rapide_solde_pour_1000"
                ]
            )
        },


        "cafes_bars": {

            "creations": valeur(
                dynamique_nantes[
                    "cafes_bars_creations"
                ]
            ),

            "fermetures": valeur(
                dynamique_nantes[
                    "cafes_bars_fermetures"
                ]
            ),

            "solde": valeur(
                dynamique_nantes[
                    "cafes_bars_solde"
                ]
            ),

            "solde_pour_1000_habitants": valeur(
                dynamique_nantes[
                    "cafes_bars_solde_pour_1000"
                ]
            )
        }
    },


    # --------------------------------------------------------
    # CONCURRENCE
    # --------------------------------------------------------

    "concurrence": {

        "hhi": valeur(
            profil_nantes["hhi"]
        ),

        "cr5_pct": valeur(
            profil_nantes["cr5_pct"]
        ),

        "cr10_pct": valeur(
            profil_nantes["cr10_pct"]
        )
    },


    # --------------------------------------------------------
    # SIGNAUX
    # --------------------------------------------------------

    "signaux": {

        "niveau_offre": valeur(
            profil_nantes["niveau_offre"]
        ),

        "dynamique_marche": valeur(
            profil_nantes["dynamique_marche"]
        ),

        "profil_marche": valeur(
            profil_nantes["profil_marche"]
        ),

        "concentration": valeur(
            profil_nantes["concentration"]
        ),

        "segment_dominant_dynamique": valeur(
            dynamique_nantes[
                "segment_dominant_dynamique"
            ]
        )
    }
}


# ============================================================
# 6. EXPORT JSON
# ============================================================

with open(
    FICHIER_SORTIE,
    "w",
    encoding="utf-8"
) as fichier:

    json.dump(
        contexte,
        fichier,
        ensure_ascii=False,
        indent=4
    )


# ============================================================
# 7. AFFICHAGE
# ============================================================

print("=" * 70)
print("CONTEXTE IA — NANTES")
print("=" * 70)

print(
    json.dumps(
        contexte,
        ensure_ascii=False,
        indent=4
    )
)

print("\n" + "=" * 70)
print(
    f"Fichier créé : {FICHIER_SORTIE}"
)
print("=" * 70)