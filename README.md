# Projet Clustering & Segmentation Clients

## Description

Cette application permet de **segmenter la clientèle** d'une entreprise en utilisant des techniques de machine learning.  
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

---

## Installation

### 1. Cloner le dépôt

```bash
git clone https://github.com/VivoAZ/Projet-clustering-/tree/master.git
cd Projet-clustering-/tree/master


### 2- Créer et activer un environnement virtuel (venv) 

python -m venv env 

source env/bin/activate  # Pour Linux/macOS 

env\Scripts\activate     # Pour Windows 

### 3- Installer les dépendances 

pip install -r requirements.txt

## Exécution 

Commande pour lancer le projet 
python main.py 

N'oubliez pas de vérifier le chemin d'accès des fichiers main.py et marketing_campaign_clean.csv selon où vous les avez sauvegardés sur votre machine. 

## Structure du projet 

main.py : Script principal pour l’entraînement et la prédiction du modèle. 

marketing_campaign_clean.csv : Contient les jeux de données bruts et transformés. 

kmeans_model.pkl : Modèle sauvegardé au format pkl.

Clustering.ipynb : Notebook Jupyter pour l’analyse exploratoire et les tests. 

requirements.txt : Liste des dépendances nécessaires. 

## Données 

Les informations proviennent de la plateforme publique Kaggle.

## Collaboration 

Si vous souhaitez contribuer :

1- Forkez le projet. 

2- Créez une branche (git checkout -b ma-branche).

3- Soumettez une Pull Request. 
