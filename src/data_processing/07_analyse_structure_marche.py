from pathlib import Path

import pandas as pd


# ============================================================
# Chemins
# ============================================================

PROJECT_DIR = Path(__file__).resolve().parents[2]

DATA_FILE = (
    PROJECT_DIR
    / "data"
    / "processed"
    / "table_analytique_restauration.csv"
)


# ============================================================
# Chargement
# ============================================================

print("Chargement de la table analytique...")

df = pd.read_csv(
    DATA_FILE,
    sep=";"
)

print(f"Nombre total d'établissements : {len(df):,}")


# ============================================================
# 1. Taille du marché
# ============================================================

print("\n" + "=" * 60)
print("1. TAILLE DU MARCHÉ")
print("=" * 60)

nombre_etablissements = len(df)

nombre_etablissements_actifs = (
    df["statut"] == "Actif"
).sum()

nombre_etablissements_fermes = (
    df["statut"] == "Fermé"
).sum()

nombre_entreprises = (
    df["siren"]
    .nunique()
)

print(
    f"Établissements : "
    f"{nombre_etablissements:,}"
)

print(
    f"Établissements actifs : "
    f"{nombre_etablissements_actifs:,}"
)

print(
    f"Établissements fermés : "
    f"{nombre_etablissements_fermes:,}"
)

print(
    f"Entreprises distinctes (SIREN) : "
    f"{nombre_entreprises:,}"
)


# ============================================================
# 2. Entreprises possédant plusieurs établissements
# ============================================================

print("\n" + "=" * 60)
print("2. ENTREPRISES MULTI-ÉTABLISSEMENTS")
print("=" * 60)

etablissements_par_entreprise = (
    df.groupby("siren")
    .size()
)

entreprises_multi = (
    etablissements_par_entreprise > 1
).sum()

etablissements_dans_entreprises_multi = (
    etablissements_par_entreprise[
        etablissements_par_entreprise > 1
    ].sum()
)

print(
    f"Entreprises possédant plusieurs établissements : "
    f"{entreprises_multi:,}"
)

print(
    f"Établissements appartenant à ces entreprises : "
    f"{etablissements_dans_entreprises_multi:,}"
)

print(
    "\nNombre maximal d'établissements pour une même entreprise :"
)

print(
    etablissements_par_entreprise.max()
)


# ============================================================
# 3. Répartition par catégorie
# ============================================================

print("\n" + "=" * 60)
print("3. RÉPARTITION PAR CATÉGORIE")
print("=" * 60)

repartition_categorie = (
    df["categorie"]
    .value_counts()
)

repartition_categorie_pourcentage = (
    df["categorie"]
    .value_counts(normalize=True)
    .mul(100)
    .round(2)
)

table_categorie = pd.DataFrame({
    "nombre": repartition_categorie,
    "pourcentage": repartition_categorie_pourcentage
})

print(table_categorie)


# ============================================================
# 4. Actifs / fermés par catégorie
# ============================================================

print("\n" + "=" * 60)
print("4. STATUT PAR CATÉGORIE")
print("=" * 60)

statut_categorie = pd.crosstab(
    df["categorie"],
    df["statut"]
)

print(statut_categorie)


# ============================================================
# 5. Taux de fermeture par catégorie
# ============================================================

print("\n" + "=" * 60)
print("5. TAUX DE FERMETURE")
print("=" * 60)

taux_fermeture = (
    df.groupby("categorie")["est_ferme"]
    .mean()
    .mul(100)
    .round(2)
    .sort_values(ascending=False)
)

print(taux_fermeture)


# ============================================================
# 6. Répartition par code NAF
# ============================================================

print("\n" + "=" * 60)
print("6. RÉPARTITION PAR CODE NAF")
print("=" * 60)

print(
    df["code_naf"]
    .value_counts()
    .sort_index()
)


# ============================================================
# 7. Résumé
# ============================================================

print("\n" + "=" * 60)
print("7. RÉSUMÉ")
print("=" * 60)

print(
    f"""
Marché étudié :
- Nantes Métropole
- Restaurants, restauration rapide et cafés/bars

Établissements :
- Total : {nombre_etablissements:,}
- Actifs : {nombre_etablissements_actifs:,}
- Fermés : {nombre_etablissements_fermes:,}

Entreprises :
- SIREN uniques : {nombre_entreprises:,}
- Entreprises multi-établissements : {entreprises_multi:,}
- Établissements dans ces entreprises : {etablissements_dans_entreprises_multi:,}
"""
)

print("Analyse terminée.")