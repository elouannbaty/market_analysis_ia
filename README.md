# Market Analysis IA

Analyse de marché et Market Intelligence appliquées au secteur de la restauration à Nantes Métropole.

## Présentation

Market Analysis IA est un projet de Data Analysis et de Market Intelligence visant à analyser le marché de la restauration à l'échelle de Nantes Métropole.

Le projet combine des données publiques, des méthodes statistiques, de l'analyse territoriale, du NLP et un LLM exécuté localement afin de transformer des données brutes en une analyse structurée du marché.

L'objectif est de construire un pipeline d'analyse reproductible et interprétable, dans lequel l'intelligence artificielle intervient comme outil de synthèse des résultats.

## Problématique

Comment exploiter des données publiques pour caractériser la structure, la dynamique et la concurrence du marché de la restauration à l'échelle territoriale, puis utiliser un LLM pour synthétiser ces résultats de manière contrôlée ?

Le projet porte sur trois segments :

- Restauration traditionnelle
- Restauration rapide
- Cafés et bars

## Données

### SIRENE

La base SIRENE de Nantes Métropole constitue la principale source utilisée pour caractériser les établissements.

Les codes NAF étudiés sont :

| Code NAF | Activité |
|---|---|
| 56.10A | Restauration traditionnelle |
| 56.10B | Cafétérias et autres libres-services |
| 56.10C | Restauration rapide |
| 56.30Z | Débits de boissons |

Après filtrage et nettoyage, le jeu de données contient 7 819 établissements.

### Insee

Les données de l'Insee permettent d'enrichir l'analyse avec des informations territoriales :

- Population
- Superficie
- Densité de population
- Niveau de vie médian
- Évolution démographique

## Analyses réalisées

### Structure du marché

Analyse de la structure du marché à partir :

- du nombre d'établissements ;
- des établissements actifs et fermés ;
- des entreprises ;
- des différents segments de restauration ;
- de la répartition géographique.

### Dynamique du marché

Analyse des créations et fermetures enregistrées dans SIRENE sur la période 2022-2025.

Cette analyse permet de comparer la dynamique globale du marché, des différents segments et des communes de Nantes Métropole.

### Analyse territoriale

Les 24 communes de Nantes Métropole sont comparées selon plusieurs indicateurs :

- nombre d'établissements actifs ;
- établissements actifs pour 1 000 habitants ;
- densité de population ;
- niveau de vie médian ;
- dynamique du marché.

Des profils territoriaux sont construits à partir de ces indicateurs.

### Analyse concurrentielle

La concentration du marché est étudiée à l'aide de :

- HHI ;
- CR5 ;
- CR10.

Ces indicateurs permettent de caractériser la concentration des établissements entre entreprises.

### Analyse textuelle

Les noms commerciaux des établissements actifs sont analysés à l'aide de :

- fréquences lexicales ;
- bigrammes ;
- TF-IDF ;
- clustering K-Means.

Cette partie permet d'identifier certains motifs lexicaux présents dans les noms commerciaux.

## Intelligence artificielle

Les résultats des analyses sont transformés en un contexte structuré par commune.

Ce contexte est ensuite transmis à un LLM exécuté localement :

**Qwen3 8B avec Ollama**

Le LLM intervient comme une couche de synthèse chargée de :

- synthétiser les résultats ;
- comparer les indicateurs ;
- mettre en évidence les principaux signaux ;
- distinguer les observations des interprétations ;
- prendre en compte les limites des données.

### Contrôle de la sortie du LLM

La sortie générée par le LLM fait l'objet d'un contrôle automatique.

Le contrôle vérifie notamment :

- la présence des sections attendues ;
- l'absence de certaines formulations problématiques ;
- la présence des principaux indicateurs quantitatifs.

Le pipeline complet est donc :

Données publiques
        ↓
Nettoyage
        ↓
Contrôle qualité
        ↓
Analyses statistiques
        ↓
Analyse territoriale
        ↓
Analyse textuelle
        ↓
Contexte structuré
        ↓
LLM local
        ↓
Synthèse Market Intelligence
        ↓
Contrôle automatique

## Architecture du projet

market_analysis_ia/
│
├── data/
│   ├── raw/
│   ├── processed/
│   └── external/
│
├── docs/
│   ├── cadrage_v0.md
│   ├── sources_donnees_v0.md
│   ├── schema_donnees_v0.md
│   └── prompt_llm_v0.md
│
├── src/
│   └── data_processing/
│
├── README.md
└── requirements.txt

Les scripts du dossier src/data_processing/ sont organisés selon les différentes étapes du pipeline, de la collecte des données jusqu'au contrôle de la sortie du LLM.

## Technologies

### Data

- Python
- Pandas
- NumPy
- SIRENE
- Insee

### Analyse

- Statistiques descriptives
- Analyse territoriale
- Corrélations
- HHI
- CR5 / CR10
- NLP
- TF-IDF
- K-Means

### Intelligence artificielle

- Ollama
- Qwen3 8B
- Prompt engineering
- Contrôle automatique des sorties

### Outils

- VS Code
- Git
- GitHub

## Résultats principaux

L'analyse permet notamment de mettre en évidence :

- une forte concentration géographique de l'offre autour des principales communes ;
- des niveaux d'offre différents selon les territoires lorsqu'ils sont rapportés à la population ;
- des dynamiques différentes selon les segments de restauration ;
- un marché globalement fragmenté à l'échelle métropolitaine ;
- des profils territoriaux différenciés selon le niveau d'offre et la dynamique observée.

Les résultats détaillés sont disponibles dans les fichiers générés du dossier data/processed/.

## Limites

Ce projet constitue un prototype de Market Intelligence et non un modèle prédictif.

Les principales limites sont :

- les créations et fermetures correspondent aux événements enregistrés dans SIRENE ;
- les données ne permettent pas de mesurer directement la rentabilité des établissements ;
- les indicateurs de concentration ne mesurent pas la performance économique ;
- les analyses territoriales sont descriptives ;
- les corrélations observées ne permettent pas d'établir de relations causales ;
- le LLM intervient comme outil de synthèse et ne produit pas de prédiction de succès ou d'échec.

Le projet ne cherche pas à produire un score arbitraire d'opportunité ou une recommandation automatique d'implantation.

## Reproductibilité

Le pipeline est organisé sous forme de scripts Python permettant de reconstruire progressivement les différentes étapes de traitement et d'analyse.

Le LLM est exécuté localement avec Ollama et Qwen3 8B.

Les sources de données, les choix méthodologiques et les règles utilisées pour l'analyse LLM sont documentés dans le dossier docs/.

## Statut

Version portfolio — V0.1

Projet réalisé comme démonstrateur de compétences en :

**Data Analysis · Statistical Analysis · Market Intelligence · NLP · Generative AI · Data Engineering**