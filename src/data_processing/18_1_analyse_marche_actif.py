from pathlib import Path

import pandas as pd


# ============================================================
# 1. PARAMÈTRES
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[2]

FICHIER_ENTREPRISES = (
    BASE_DIR
    / "data"
    / "processed"
    / "analyse_entreprises_restauration.csv"
)

FICHIER_SIRENE = (
    BASE_DIR
    / "data"
    / "processed"
    / "table_analytique_restauration.csv"
)

FICHIER_SORTIE = (
    BASE_DIR
    / "data"
    / "processed"
    / "marche_actif_restauration.csv"
)


# ============================================================
# 2. CHARGEMENT
# ============================================================

df = pd.read_csv(
    FICHIER_SIRENE,
    sep=";",
    low_memory=False
)


# ============================================================
# 3. FILTRE : ÉTABLISSEMENTS ACTIFS
# ============================================================

df_actif = df[
    df["est_ferme"] == False
].copy()


# ============================================================
# 4. NORMALISATION DE L'ENSEIGNE
# ============================================================

df_actif["enseigne"] = (
    df_actif["enseigne_1"]
    .fillna("")
    .astype(str)
    .str.strip()
)

df_actif["enseigne_renseignee"] = (
    df_actif["enseigne"] != ""
)


# ============================================================
# 5. NOMBRE D'ÉTABLISSEMENTS ACTIFS PAR SIREN
# ============================================================

nb_actifs_par_siren = (
    df_actif
    .groupby("siren")
    .agg(
        etablissements_actifs=("siret", "nunique")
    )
    .reset_index()
)


# ============================================================
# 6. TYPE D'ACTEUR
# ============================================================

nb_actifs_par_siren["type_acteur"] = "Mono-établissement"

nb_actifs_par_siren.loc[
    nb_actifs_par_siren["etablissements_actifs"] > 1,
    "type_acteur"
] = "Multi-établissements"


# ============================================================
# 7. AJOUT DU TYPE D'ACTEUR AUX ÉTABLISSEMENTS
# ============================================================

df_actif = df_actif.merge(
    nb_actifs_par_siren[
        [
            "siren",
            "etablissements_actifs",
            "type_acteur"
        ]
    ],
    on="siren",
    how="left"
)


# ============================================================
# 8. STATISTIQUES GÉNÉRALES
# ============================================================

nombre_actifs = len(df_actif)

nombre_siren_actifs = (
    df_actif["siren"]
    .nunique()
)

nombre_mono = (
    nb_actifs_par_siren["type_acteur"]
    .eq("Mono-établissement")
    .sum()
)

nombre_multi = (
    nb_actifs_par_siren["type_acteur"]
    .eq("Multi-établissements")
    .sum()
)

actifs_multi = (
    df_actif[
        df_actif["type_acteur"]
        == "Multi-établissements"
    ]
    .shape[0]
)

part_actifs_multi = (
    actifs_multi
    / nombre_actifs
    * 100
)


# ============================================================
# 9. TOP ENSEIGNES ACTIVES
# ============================================================

top_enseignes = (
    df_actif[
        df_actif["enseigne_renseignee"]
    ]
    .groupby("enseigne")
    .agg(
        etablissements_actifs=("siret", "nunique"),
        entreprises=("siren", "nunique"),
        communes=("commune", "nunique"),
        categorie_principale=(
            "categorie",
            lambda x: (
                x.mode().iloc[0]
                if not x.mode().empty
                else "Inconnue"
            )
        )
    )
    .reset_index()
    .sort_values(
        [
            "etablissements_actifs",
            "entreprises"
        ],
        ascending=False
    )
)


# ============================================================
# 10. PART DE MARCHÉ DES ENSEIGNES
# ============================================================

top_enseignes["part_offre_active"] = (
    top_enseignes["etablissements_actifs"]
    / nombre_actifs
    * 100
)


# ============================================================
# 11. CONCENTRATION PAR ENTREPRISE
# ============================================================

concentration = (
    nb_actifs_par_siren
    .sort_values(
        "etablissements_actifs",
        ascending=False
    )
    .reset_index(drop=True)
)


concentration["part_offre_active"] = (
    concentration["etablissements_actifs"]
    / nombre_actifs
    * 100
)


# ============================================================
# 12. PART DU TOP 10 DES ENTREPRISES
# ============================================================

top10_part = (
    concentration
    .head(10)["etablissements_actifs"]
    .sum()
    / nombre_actifs
    * 100
)


# ============================================================
# 13. HHI
# ============================================================

parts_marche = (
    concentration["etablissements_actifs"]
    / nombre_actifs
)

hhi = (
    (parts_marche ** 2)
    .sum()
    * 10000
)


# ============================================================
# 14. PART DES ENSEIGNES RENSEIGNÉES
# ============================================================

nombre_enseigne_renseignee = (
    df_actif["enseigne_renseignee"]
    .sum()
)

part_enseigne_renseignee = (
    nombre_enseigne_renseignee
    / nombre_actifs
    * 100
)


# ============================================================
# 15. EXPORT
# ============================================================

resultat = df_actif[
    [
        "siret",
        "siren",
        "categorie",
        "commune",
        "enseigne",
        "type_acteur",
        "etablissements_actifs",
        "enseigne_renseignee"
    ]
].copy()


resultat.to_csv(
    FICHIER_SORTIE,
    sep=";",
    index=False
)


# ============================================================
# 16. AFFICHAGE
# ============================================================

print("=" * 70)
print("PHOTOGRAPHIE DU MARCHÉ ACTIF")
print("=" * 70)

print(
    f"\nÉtablissements actifs : "
    f"{nombre_actifs}"
)

print(
    f"Entreprises / SIREN actives : "
    f"{nombre_siren_actifs}"
)

print(
    f"Acteurs mono-établissement : "
    f"{nombre_mono}"
)

print(
    f"Acteurs multi-établissements : "
    f"{nombre_multi}"
)

print(
    f"Établissements appartenant à "
    f"des multi-établissements : "
    f"{actifs_multi}"
)

print(
    f"Part de l'offre détenue par ces acteurs : "
    f"{part_actifs_multi:.2f}%"
)

print(
    f"\nEnseignes renseignées : "
    f"{nombre_enseigne_renseignee}"
)

print(
    f"Part des établissements actifs avec "
    f"une enseigne renseignée : "
    f"{part_enseigne_renseignee:.2f}%"
)

print(
    f"\nPart des 10 plus grandes entreprises : "
    f"{top10_part:.2f}%"
)

print(
    f"HHI par entreprise : "
    f"{hhi:.2f}"
)


print("\nTop 20 des enseignes actives :")

print(
    top_enseignes[
        [
            "enseigne",
            "etablissements_actifs",
            "entreprises",
            "communes",
            "part_offre_active",
            "categorie_principale"
        ]
    ]
    .head(20)
    .to_string(index=False)
)


print("\nTop 15 des entreprises par nombre "
      "d'établissements actifs :")

print(
    concentration[
        [
            "siren",
            "etablissements_actifs",
            "part_offre_active",
            "type_acteur"
        ]
    ]
    .head(15)
    .to_string(index=False)
)


print("\n" + "=" * 70)
print(
    f"Fichier créé : {FICHIER_SORTIE}"
)
print("=" * 70)