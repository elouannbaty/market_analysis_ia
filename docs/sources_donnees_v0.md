# Market Analysis IA — Sources de données V0

## 1. Objectif

Ce document recense les sources de données utilisées ou envisagées pour la V0 du projet Market Analysis IA.

Les sources sont sélectionnées selon plusieurs critères :

- pertinence pour l'analyse du marché de la restauration ;
- qualité et documentation des données ;
- accessibilité ;
- reproductibilité ;
- conditions de réutilisation ;
- possibilité d'automatisation ;
- capacité à être intégrées dans une architecture de données cohérente.

---

## 2. Sources principales

### 2.1 SIRENE — Nantes Métropole

**Producteur :** INSEE / Nantes Métropole

**Type :** données administratives et économiques sur les établissements

**Territoire :** Nantes Métropole

**Utilisation dans le projet :**

- identifier les établissements ;
- filtrer les activités liées à la restauration ;
- analyser la répartition géographique ;
- étudier les dates de création et de fermeture ;
- exploiter les informations relatives aux effectifs ;
- constituer la base principale des établissements.

**Variables potentielles :**

- SIRET ;
- SIREN ;
- code NAF ;
- libellé de l'activité ;
- état administratif ;
- date de création ;
- date de fermeture ;
- commune ;
- code commune ;
- adresse ;
- code postal ;
- géolocalisation ;
- tranche d'effectif ;
- enseigne ;
- dénomination usuelle.

**Source :**

Base SIRENE des entreprises de Nantes Métropole.

---

### 2.2 Restaurants en Loire-Atlantique — e-SPRIT

**Producteur :** réseau e-SPRIT / Loire-Atlantique Open Data

**Type :** données spécialisées sur les restaurants

**Territoire :** Loire-Atlantique

**Utilisation dans le projet :**

- compléter les informations issues de SIRENE ;
- identifier les établissements de restauration ;
- récupérer des informations spécifiques au secteur touristique ;
- enrichir les caractéristiques des restaurants ;
- étudier les informations textuelles disponibles.

**Formats disponibles :**

- CSV ;
- JSON ;
- XML ;
- XLS ;
- API.

**Source :**

Jeu de données « Restaurants en Loire-Atlantique ».

---

### 2.3 Données territoriales INSEE

**Producteur :** INSEE

**Type :** données démographiques et territoriales

**Territoire :** Nantes Métropole

**Utilisation dans le projet :**

- contextualiser la présence des établissements ;
- calculer des indicateurs rapportés à la population ;
- comparer les territoires ;
- analyser la densité de l'offre ;
- enrichir les analyses territoriales.

**Variables potentielles :**

- population ;
- densité de population ;
- nombre d'habitants ;
- caractéristiques démographiques ;
- variables territoriales disponibles à une échelle pertinente.

---

## 3. Sources secondaires potentielles

Certaines sources pourront être ajoutées ultérieurement si elles apportent une réelle valeur analytique.

### 3.1 OpenStreetMap

Utilisation potentielle :

- enrichissement géographique ;
- catégories d'établissements ;
- informations sur les commerces et points d'intérêt ;
- données géographiques complémentaires.

Cette source n'est pas encore intégrée à la V0.

### 3.2 Autres sources textuelles

Des sources textuelles publiques pourront éventuellement être étudiées afin d'enrichir la composante NLP/IA.

Elles ne seront intégrées qu'après vérification de leur accessibilité, de leur qualité et de leurs conditions de réutilisation.

---

## 4. Principe de sélection

La V0 privilégie les sources :

1. publiques ;
2. documentées ;
3. reproductibles ;
4. légalement réutilisables ;
5. suffisamment stables ;
6. pertinentes pour les objectifs du projet.

Une source ne sera intégrée que si sa valeur ajoutée est suffisante par rapport à sa complexité d'exploitation.

---

## 5. Architecture des données

Les données suivront le principe :

Source externe
→ données brutes
→ nettoyage
→ données transformées
→ base analytique
→ analyses
→ restitution.

Les données originales téléchargées seront conservées dans `data/raw/`.

Les données transformées seront stockées dans `data/processed/`.

Les données complémentaires et référentiels externes seront stockés dans `data/external/`.