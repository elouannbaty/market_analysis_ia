from pathlib import Path

import pandas as pd


# ============================================================
# 1. PARAMÈTRES
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[2]

FICHIER_SOURCE = (
    BASE_DIR
    / "data"
    / "processed"
    / "table_analytique_restauration.csv"
)

FICHIER_SORTIE = (
    BASE_DIR
    / "data"
    / "processed"
    / "concentration_marche_restauration.csv"
)

SEUIL_COMMUNE = 30


# ============================================================
# 2. CHARGEMENT
# ============================================================

df = pd.read_csv(
    FICHIER_SOURCE,
    sep=";",
    low_memory=False
)


# ============================================================
# 3. MARCHÉ ACTIF
# ============================================================

df = df[
    df["est_ferme"] == False
].copy()


# ============================================================
# 4. FONCTION DE CONCENTRATION
# ============================================================

def indicateurs_concentration(groupe):

    total = len(groupe)

    parts = (
        groupe
        .groupby("siren")["siret"]
        .count()
        / total
        * 100
    )

    hhi = (parts ** 2).sum()

    cr5 = parts.sort_values(
        ascending=False
    ).head(5).sum()

    cr10 = parts.sort_values(
        ascending=False
    ).head(10).sum()

    return hhi, cr5, cr10


# ============================================================
# 5. MARCHÉ GLOBAL
# ============================================================

hhi_global, cr5_global, cr10_global = (
    indicateurs_concentration(df)
)


print("=" * 70)
print("CONCENTRATION DU MARCHÉ ACTIF")
print("=" * 70)

print(
    f"\nÉtablissements actifs : {len(df)}"
)

print(
    f"Entreprises actives : {df['siren'].nunique()}"
)

print(
    f"HHI global : {hhi_global:.2f}"
)

print(
    f"CR5 global : {cr5_global:.2f} %"
)

print(
    f"CR10 global : {cr10_global:.2f} %"
)


# ============================================================
# 6. CONCENTRATION PAR CATÉGORIE
# ============================================================

resultats = []

for categorie, groupe in df.groupby("categorie"):

    hhi, cr5, cr10 = (
        indicateurs_concentration(groupe)
    )

    resultats.append(
        {
            "niveau": "categorie",
            "territoire": "Nantes Métropole",
            "categorie": categorie,
            "etablissements_actifs": len(groupe),
            "entreprises_actives": groupe["siren"].nunique(),
            "hhi": round(hhi, 2),
            "cr5_pct": round(cr5, 2),
            "cr10_pct": round(cr10, 2),
        }
    )


# ============================================================
# 7. CONCENTRATION PAR COMMUNE
# ============================================================

for commune, groupe in df.groupby("commune"):

    # On ignore les communes trop petites
    if len(groupe) < SEUIL_COMMUNE:
        continue

    hhi, cr5, cr10 = (
        indicateurs_concentration(groupe)
    )

    resultats.append(
        {
            "niveau": "commune",
            "territoire": commune,
            "categorie": "Toutes catégories",
            "etablissements_actifs": len(groupe),
            "entreprises_actives": groupe["siren"].nunique(),
            "hhi": round(hhi, 2),
            "cr5_pct": round(cr5, 2),
            "cr10_pct": round(cr10, 2),
        }
    )


resultats = pd.DataFrame(resultats)


# ============================================================
# 8. RÉSULTATS PAR CATÉGORIE
# ============================================================

print("\n" + "=" * 70)
print("CONCENTRATION PAR CATÉGORIE")
print("=" * 70)

categories = (
    resultats[
        resultats["niveau"] == "categorie"
    ]
    .sort_values(
        "cr5_pct",
        ascending=False
    )
)

for _, ligne in categories.iterrows():

    print(
        f"{ligne['categorie']:<25} "
        f"HHI = {ligne['hhi']:>7.2f} "
        f"| CR5 = {ligne['cr5_pct']:>6.2f} % "
        f"| CR10 = {ligne['cr10_pct']:>6.2f} %"
    )


# ============================================================
# 9. RÉSULTATS PAR COMMUNE
# ============================================================

print("\n" + "=" * 70)
print(
    f"CONCENTRATION PAR COMMUNE "
    f"(≥ {SEUIL_COMMUNE} établissements actifs)"
)
print("=" * 70)

communes = resultats[
    resultats["niveau"] == "commune"
].sort_values(
    "cr5_pct",
    ascending=False
)


print("\n--- CR5 LE PLUS ÉLEVÉ ---")

print(
    communes[
        [
            "territoire",
            "etablissements_actifs",
            "entreprises_actives",
            "hhi",
            "cr5_pct",
            "cr10_pct",
        ]
    ]
    .head(10)
    .to_string(index=False)
)


print("\n--- CR5 LE PLUS FAIBLE ---")

print(
    communes[
        [
            "territoire",
            "etablissements_actifs",
            "entreprises_actives",
            "hhi",
            "cr5_pct",
            "cr10_pct",
        ]
    ]
    .sort_values("cr5_pct")
    .head(10)
    .to_string(index=False)
)


# ============================================================
# 10. EXPORT
# ============================================================

resultats.to_csv(
    FICHIER_SORTIE,
    sep=";",
    index=False
)


print("\n" + "=" * 70)

print(
    f"Fichier créé : {FICHIER_SORTIE}"
)

print("=" * 70)