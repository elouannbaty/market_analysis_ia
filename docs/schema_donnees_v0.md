# Market Analysis IA — Schéma des données V0

## 1. Objectif

La V0 repose sur plusieurs sources de données complémentaires.

La base principale sera constituée des établissements issus de SIRENE sur le territoire de Nantes Métropole.

Cette base sera enrichie par :

* les données spécialisées sur les restaurants ;
* les données territoriales ;
* des variables calculées pour les analyses statistiques et géographiques.

L'objectif est de construire une base analytique suffisamment structurée pour permettre :

* l'analyse du marché ;
* l'analyse territoriale ;
* l'analyse concurrentielle ;
* l'analyse temporelle ;
* l'analyse textuelle ;
* la génération de synthèses par intelligence artificielle.

---

## 2. Source SIRENE

### 2.1 Identification

Variables retenues :

* `siret`
* `siren`
* `etat_administratif_etablissement`
* `etablissement_siege`

Le SIRET constituera l'identifiant principal de l'établissement.

---

### 2.2 Localisation

Variables retenues :

* `code_postal_etablissement`
* `commune_etablissement`
* `code_commune_etablissement`
* `adresse_etablissement`
* `geolocalisation`
* `code_epci`
* `libelle_epci`

Ces variables permettront notamment :

* de localiser les établissements ;
* de réaliser des analyses par commune ;
* de produire des cartes ;
* de calculer des indicateurs territoriaux ;
* de croiser l'offre avec les données démographiques.

---

### 2.3 Activité

Variables retenues :

* `activite_principale_etablissement`
* `libelle_activite_principale_etablissement`
* `section_naf`
* `division_naf`
* `groupe_naf`
* `classe_naf`

Le périmètre principal de la V0 sera constitué des activités suivantes :

| Code NAF | Activité                             |
| -------- | ------------------------------------ |
| `56.10A` | Restauration traditionnelle          |
| `56.10B` | Cafétérias et autres libres-services |
| `56.10C` | Restauration de type rapide          |
| `56.30Z` | Débits de boissons                   |

Les activités de traiteur, restauration collective et autres activités de restauration ne seront pas intégrées au périmètre principal de la V0.

---

### 2.4 Caractéristiques de l'établissement

Variables retenues :

* `tranche_effectif_etablissement`
* `caractere_employeur_etablissement`
* `categorie_entreprise`
* `denomination_usuelle_etablissement`
* `enseigne`

Ces variables permettront notamment d'étudier :

* la taille des établissements ;
* la structure du marché ;
* la concentration géographique ;
* les enseignes présentes ;
* les différences entre établissements indépendants et structures plus importantes lorsque l'information est disponible.

---

### 2.5 Informations temporelles

Variables retenues :

* `date_creation_etablissement`
* `date_fermeture_etablissement`
* `date_derniere_mise_a_jour`
* `date_debut_periode`

Ces variables seront utilisées pour construire :

* les créations d'établissements ;
* les fermetures d'établissements ;
* l'évolution du parc ;
* des indicateurs d'ancienneté ;
* des analyses temporelles.

---

## 3. Source Restaurants en Loire-Atlantique

### 3.1 Identification

Variables recherchées :

* identifiant de l'établissement lorsqu'il existe ;
* nom de l'établissement ;
* identifiant touristique lorsqu'il existe.

Cette source sera utilisée principalement comme source d'enrichissement.

---

### 3.2 Localisation

Variables recherchées :

* adresse ;
* commune ;
* code postal ;
* coordonnées géographiques ;
* identifiants géographiques disponibles.

Ces informations pourront permettre :

* de compléter la localisation ;
* de contrôler certaines coordonnées ;
* de réaliser une correspondance avec les établissements SIRENE.

---

### 3.3 Caractéristiques

Variables recherchées :

* type d'établissement ;
* type de cuisine ;
* services ;
* équipements ;
* capacité ;
* gamme ou catégorie lorsqu'elle est disponible ;
* labels éventuels.

Seules les variables réellement présentes et suffisamment complètes dans la source seront conservées.

---

### 3.4 Informations textuelles

Les champs textuels disponibles seront étudiés afin d'alimenter la composante NLP/IA.

Variables potentielles :

* description ;
* présentation ;
* prestations ;
* spécialités ;
* type de cuisine ;
* informations complémentaires.

Les textes pourront être utilisés pour :

* identifier des thèmes ;
* caractériser les établissements ;
* calculer des similarités ;
* construire des représentations sémantiques ;
* produire des synthèses avec un LLM.

---

## 4. Données territoriales

Les données territoriales permettront de contextualiser l'offre de restauration.

Variables potentielles :

* population ;
* densité de population ;
* superficie ;
* nombre d'habitants ;
* indicateurs démographiques ;
* identifiant géographique.

L'échelle privilégiée sera la commune ou une échelle territoriale compatible avec les données disponibles.

Ces données permettront notamment de calculer :

* restaurants pour 1 000 habitants ;
* densité d'établissements ;
* comparaison entre communes ;
* concentration territoriale de l'offre.

---

## 5. Variables retenues

La base analytique finale devra notamment contenir les familles de variables suivantes :

### Identification

* `siret`
* `siren`
* `nom_etablissement`

### Activité

* `code_naf`
* `libelle_naf`
* `categorie_activite`

### Localisation

* `code_commune`
* `commune`
* `code_postal`
* `adresse`
* `latitude`
* `longitude`

### Structure

* `tranche_effectif`
* `caractere_employeur`
* `categorie_entreprise`

### Temporalité

* `date_creation`
* `date_fermeture`
* `date_mise_a_jour`

### Enrichissement

* `type_cuisine`
* `services`
* `capacite`
* `description`
* autres variables pertinentes disponibles dans la source restaurant.

---

## 6. Variables calculées

Les variables suivantes seront créées lors de la phase de transformation.

### Variables temporelles

* `annee_creation`
* `annee_fermeture`
* `anciennete`
* `statut_actuel`

### Variables géographiques

* `latitude`
* `longitude`
* `commune`
* `densite_restaurants_commune`

### Variables de marché

* `categorie_activite`
* `nombre_etablissements_commune`
* `part_categorie_activite`
* `restaurants_pour_1000_habitants`

### Variables textuelles

Selon les données disponibles :

* `texte_normalise`
* `longueur_description`
* `theme_principal`
* `embedding`
* `similarite_semantique`

Les embeddings et variables issues des modèles d'IA seront séparés des données sources originales.

---

## 7. Clés de correspondance

La clé de référence principale sera :

`SIRET`

Lorsque le SIRET est disponible dans les deux sources, il sera utilisé pour effectuer la correspondance.

Lorsque le SIRET n'est pas disponible dans la source restaurant, une correspondance secondaire pourra être étudiée à partir de :

* nom ;
* adresse ;
* commune ;
* coordonnées géographiques.

Cette correspondance secondaire devra être contrôlée afin de limiter les faux rapprochements.

Aucune correspondance approximative ne sera considérée comme certaine sans contrôle.

---

## 8. Données exclues

Les données suivantes seront exclues de la V0 lorsqu'elles ne présentent pas de valeur analytique directe :

* données personnelles inutiles à l'analyse ;
* informations administratives sans intérêt pour le marché ;
* variables redondantes ;
* variables très fortement incomplètes sans intérêt analytique ;
* données non documentées ;
* données dont les conditions de réutilisation ne sont pas suffisamment claires.

Les données originales ne seront pas modifiées.

Les traitements seront réalisés dans des fichiers ou tables séparés afin de conserver une séparation claire entre :

**données brutes → données nettoyées → données analytiques → résultats d'analyse → résultats IA.**
