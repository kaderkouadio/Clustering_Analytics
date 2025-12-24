# Clustering Analytics Dashboard : Segmentation Marketing & Dashboard Interactif

Bienvenue dans la **Phase Finale** de **Clustering Analytics Dashboard**, une solution complète full-stack de **segmentation client avancée** basée sur le dataset Marketing Campaign (UCI/Kaggle).  
Cette phase conclut un projet 100 % production-ready : de l ingestion des données jusqu’à un dashboard analytique interactif, en passant par une API FastAPI ultra-robuste et un pipeline ML supervisé/non supervisé.

Ce projet illustre des compétences de haut niveau en **Data Engineering, Machine Learning Engineering, Backend Development, et Data Visualization**.

### Description

Cette application permet de **segmenter la clientèle** dune entreprise en utilisant des techniques de machine learning.  
Elle combine un **dashboard interactif Streamlit**, un **API FastAPI** pour les prédictions et un modèle de clustering pour l’analyse des clients.  

Objectifs principaux :  
- Identifier les segments clients (VIP, à réactiver, jeunes potentiels…).  
- Proposer des **actions marketing personnalisées**.  
- Optimiser le budget des campagnes.  

---

## Fonctionnalités

1. **Segmentation Clients (Dashboard Streamlit)**  
   - Projection PCA des clients existants.  
   - Visualisation des segments (Nuage PCA, Répartition, Profils moyens).  

2. **Exploration Libre de Données**  
   - Upload de fichiers CSV ou Excel.  
   - Analyse univariée et bivariée.  
   - KPIs personnalisés et statistiques descriptives.  

3. **Prédiction & Recommandations Marketing**  
   - Formulaire complet pour saisir les caractéristiques d’un client.  
   - Prédiction du segment via **FastAPI** ou **modèle local**.  
   - Recommandations marketing et actions concrètes à lancer.  
   - Visualisation du client dans le nuage PCA (mode local).  


## Aperçu de la Phase Finale

**Objectif** : Transformer des données brutes clients en **4 segments marketing actionnables** avec stratégie dédiée, prédiction en temps réel, et visualisation intuitive — le tout accessible via une application web moderne et déployée en production.

- **Pipeline ML complet** :
  - Clustering non supervisé (KMeans)
  - Classifieur supervisé (RandomForest → 99.1 % accuracy)
  - Réduction dimensionnelle PCA (2D)
  - Mapping métier automatique (Premium VIP, Jeunes à Potentiel, etc.)
- **API FastAPI production-grade** :
  - 12 endpoints (prédiction, PCA, santé, stats, sauvegarde BDD)
  - Logging, CORS, gestion d’erreurs globale, Swagger UI
- **Dashboard Streamlit multi-pages** :
  - Design premium, interactivité totale, état des artefacts en temps réel

**Livrables** :
- API déployée : `https://clustering-api-kader.onrender.com/docs`
- Dashboard live : `https://clustering-dashboard-kader.streamlit.app`
- Artefacts ML + base SQLite fonctionnelle

**Contexte des phases précédentes** :  
Phase 1 → Pipeline ELT + entraînement modèles  
Phase 2 → API FastAPI robuste avec prédiction temps réel  
Phase 3 → Dashboard analytique & visualisation PCA

---

## Structure du Projet

---

## Technologies Utilisées

- **Python 3.11** : Langage principal
- **FastAPI** : API RESTful ultra-rapide
- **Scikit-learn** : KMeans, RandomForest, PCA, Pipeline
- **Pydantic v2** : Validation stricte des données
- **SQLite** : Stockage des prédictions
- **Streamlit** : Application web interactive
- **Plotly** : Visualisations dynamiques
- **Joblib** : Sauvegarde des modèles
- **Render** : Hébergement gratuit (API + Dashboard)
- **Docker** : Conteneurisation complète

---

## Détails de la Phase Finale

### 1. Pipeline Machine Learning & Mapping Métier
- **Clustering** : KMeans (k=4) sur données préprocessées
- **Prédiction supervisée** : RandomForest entraîné sur les labels KMeans → **99.1 % accuracy**
- **PCA 2D** : Projection complète du dataset + nouveaux clients
- **Mapping métier intégré** :
  - Premium VIP → Haut revenu, achats fréquents
  - Jeunes à Potentiel → Moins de 40 ans, fort potentiel futur
  - Équilibrés → Clientèle stable et rentable
  - Limités → Faible engagement, risque de churn

### 2. API FastAPI Production-Ready
- **Endpoints clés** :
  - `/predict-cluster` → Prédiction instantanée d’un client
  - `/cluster` → Clustering batch + stratégie marketing complète
  - `/apply-pca` → Projection PCA en temps réel
  - `/pca` & `/segments/stats` → Données pour le frontend
  - `/health` & `/metadata` → Monitoring & traçabilité
  - `/save-prediction` → Persistance en base PostgreSQL
- **Robustesse** :
  - Chargement des modèles au startup
  - Gestion globale des erreurs
  - Logging détaillé
  - CORS activé
  - Swagger UI magnifique

### 3. Application Streamlit (Frontend)
- **Structure multi-pages** :
  - `dashboard.py` → Navigation élégante
  - `page_home.py` → Présentation, état des artefacts, test API
  - `page_explore.py` → Nuage PCA interactif + profils détaillés
  - `page_predict.py` → Saisie manuelle ou upload CSV → segment + recommandation
- **Design premium** :
  - Header dégradé vert
  - Profil + lien LinkedIn
  - État des artefacts en temps réel
  - Footer professionnel

---

## Mise en Place de l’Environnement

### Prérequis
- Python 3.11+
- VSCode (recommandé)
- Git & GitHub
- Compte Render (gratuit)
- (Optionnel) PostgreSQL local ou via Docker

### Étapes d’Installation

1. **Cloner le dépôt**
   ```bash
   git clone https://github.com/kaderkouadio/Projet_clustering.git
   
   cd Projet_clustering



2. Créer l’environnement virtuel
   ```bash
   python -m venv venv
   source venv/bin/activate        # Linux/Mac
   .\venv\Scripts\activate       # Windows


3.  Installer les dépendances
    ```bash
    pip install -r Backend/Api/requirements.txt
    pip install -r Frontend/requirements.txt

4. Placer les artefacts ML dans Data/

5. Lancer l’API
   ```bash
   cd Backend/Api
   uvicorn main:app --reload --port 8001

6. Lancer le Dashboard
   ```bash
   cd Frontend/
   streamlit run dashboard.py

---

Utilisation de l’Application

- Accueil : Vue d’ensemble du projet, état des modèles, test API en direct

- Analyse exploratoire : Nuage de points PCA interactif, statistiques par segment

- Prédiction : Saisir les données d’un client → segment + stratégie marketing instantanée


---

Déploiement Cloud (Render – 100 % gratuit)

API → Web Service (Python)
Dashboard → Web Service (Streamlit)
Variables d’environnement:

API_BASE_URL=https://clustering-api-kader.onrender.com

---

Liens déjà déployés :

API + Swagger → https://clustering-api-kader.onrender.com/docs

Dashboard → https://clustering-dashboard-kader.streamlit.app

---

7. Docker (optionnel):
   ```bash
   docker-compose up -d


---

Réalisations Clés

- Pipeline ML complet : KMeans + RandomForest supervisé + PCA

- API production-grade : 99.1 % accuracy, monitoring, sauvegarde BDD

- Dashboard premium : Design soigné, interactivité totale

- Déploiement full cloud : Render + liens live fonctionnels

- Impact business immédiat : 4 segments avec stratégie marketing précise


---

**Pourquoi Ce Projet Se Démarque** 

Ce projet démontre une maîtrise complète de la chaîne Data → ML → Backend → Frontend → DevOps :

Architecture full-stack irréprochable
Code propre, typé, documenté, testé
Prédiction fiable à 99.1 %
Interface utilisateur magnifique
Déploiement en production en 5 minutes

C’est exactement le type de projet qui fait dire aux recruteurs : « On l’embauche demain. »


----

## Améliorations Futures

- Système de recommandation personnalisée (Association Rules / Deep Learning)

- Alerting churn automatique

- Intégration CRM (Salesforce, HubSpot)

- Version React/Vue du dashboard

- Monitoring ML avec Evidently AI

----

## Liens Utiles

API Live + Documentation → https://clustering-api-kader.onrender.com/docs

Dashboard Interactif → https://clustering-dashboard-kader.streamlit.app

Code source complet → https://github.com/kaderkouadio/Clustering_Analytics

---

## Contact
Pour toute question ou collaboration, n’hésitez pas à me contacter :

- **LinkedIn** : [Koukou Kader Kouadio](https://www.linkedin.com/in/koukou-kader-kouadio-2a32371a4/)
- **Email** : [kkaderkouadio@gmail.com](mailto:kkaderkouadio@gmail.com)


Merci d’avoir exploré Clustering Analytics Dashboard !
Ce projet est le fruit de centaines d’heures de travail, de passion et de rigueur technique.
Il est conçu pour impressionner, convaincre, et prouver que je suis prêt à générer de la valeur dès le premier jour.

À très bientôt,


# **Kader KOUADIO**
  ```bash  
  Économiste • Analyste Financier • Data Analyst • Développeur BI & Intelligence Artificielle
 