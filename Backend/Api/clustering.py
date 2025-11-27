
# ============================================================
#     SCRIPT : Clustering Marketing Clients
#     Auteur : Kader KOUADIO
#     Description : Prétraitement, PCA, KMeans, CAH, Analyse
# ============================================================

"""
train_and_save_models.py
========================

But :
- Charger le dataset marketing
- Prétraiter (création Age, Customer_Seniority ; imputation)
- Construire un preprocessor (StandardScaler + OneHotEncoder)
- Appliquer KMeans pour segmenter (labels non supervisés)
- Entraîner un classifieur supervisé qui reproduit ces labels (pour prédictions rapides)
- Calculer et sauvegarder une PCA (2D) pour visualisation
- Sauvegarder tous les artefacts dans processed_data/

Usage :
    python train_and_save_models.py

Sorties :
- processed_data/preprocessor.joblib
- processed_data/kmeans_model.joblib
- processed_data/pca_model.joblib
- processed_data/classifier_best.joblib
- processed_data/features_list.json
- processed_data/model_metadata.json
"""

import os
import json
from datetime import datetime
import joblib
import numpy as np
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
from sklearn.pipeline import Pipeline
from pathlib import Path


# -------------------------
# Configuration des chemins
# -------------------------

# Dossier actuel : Backend/Api/
CURRENT_DIR = Path(__file__).resolve().parent

# Dossier racine du projet : remonte Backend → racine
PROJECT_DIR = CURRENT_DIR.parent.parent

# Dossier Data à la racine
DATA_DIR = PROJECT_DIR / "Data"
PROCESSED_DIR = PROJECT_DIR / "Data"   # même dossier ici

# Création si n'existent pas
DATA_DIR.mkdir(parents=True, exist_ok=True)

# Chemins des fichiers
CSV_PATH = DATA_DIR / "marketing_campaign_clean.csv"
PREPROCESSOR_PATH = DATA_DIR / "preprocessor.joblib"
KMEANS_PATH = DATA_DIR / "kmeans_model.joblib"
PCA_PATH = DATA_DIR / "pca_model.joblib"
CLASSIFIER_PATH = DATA_DIR / "classifier_best.joblib"
FEATURES_JSON = DATA_DIR / "features_list.json"
METADATA_JSON = DATA_DIR / "model_metadata.json"
PCA_COORDS_CSV = DATA_DIR / "pca_coords.csv"


# -------------------------
# Features (mêmes que ton script)
# -------------------------
categorical_features = ['Education', 'Marital_Status']
numeric_features = [
    'Age', 'Customer_Seniority', 'Income', 'Kidhome', 'Teenhome', 'Recency',
    'MntWines','MntFruits','MntMeatProducts','MntFishProducts','MntSweetProducts','MntGoldProds',
    'NumDealsPurchases','NumWebPurchases','NumCatalogPurchases','NumStorePurchases','NumWebVisitsMonth'
]
ALL_FEATURES = numeric_features + categorical_features

# -------------------------
# Fonctions utilitaires
# -------------------------
def load_and_prep(path: str) -> pd.DataFrame:
    """
    Charge le CSV et applique le prétraitement identique à ton script :
      - imputation Income
      - conversion Dt_Customer
      - calcul Customer_Seniority
      - calcul Age
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"CSV not found: {path}. Place your CSV in `{path}`")

    df = pd.read_csv(path, sep=";")
    # Imputation simple
    df["Income"] = df["Income"].fillna(df["Income"].mean())

    # Date -> ancienneté
    df["Dt_Customer"] = pd.to_datetime(df["Dt_Customer"], format="%d-%m-%Y", errors="coerce")
    today = pd.to_datetime("today")
    df["Customer_Seniority"] = (today - df["Dt_Customer"]).dt.days

    # Age
    df["Age"] = datetime.now().year - df["Year_Birth"]

    # On garde seulement les colonnes nécessaires + dropna
    df_sel = df[ALL_FEATURES].copy()
    df_sel = df_sel.dropna().reset_index(drop=True)
    return df_sel

def build_preprocessor():
    """
    Construit et retourne un ColumnTransformer :
      - StandardScaler pour les features numériques
      - OneHotEncoder(handle_unknown='ignore') pour les catégoriques
    """
    from sklearn.compose import ColumnTransformer
    from sklearn.preprocessing import StandardScaler, OneHotEncoder

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", StandardScaler(), numeric_features),
            ("cat", OneHotEncoder(handle_unknown="ignore", sparse_output=False), categorical_features),
        ],
        remainder="drop"
    )

    return preprocessor

# -------------------------
# Pipeline d'entraînement
# -------------------------
def main():
    print("=== Chargement des données ===")
    df = load_and_prep(CSV_PATH)
    print(f"Dataset shape after select/dropna: {df.shape}")

    # Save feature list for later inference (order matters)
    with open(FEATURES_JSON, "w") as f:
        json.dump(ALL_FEATURES, f, indent=2)
    print("Features saved to", FEATURES_JSON)

    # Preprocessor
    print("=== Construction du préprocesseur ===")
    preprocessor = build_preprocessor()
    X_pre = preprocessor.fit_transform(df)  # numpy array
    joblib.dump(preprocessor, PREPROCESSOR_PATH)
    print("Preprocessor saved ->", PREPROCESSOR_PATH)
    print("Transformed shape:", X_pre.shape)

    # KMeans (unsupervised labels)
    print("=== Entraînement KMeans (pour générer labels) ===")
    K = 4
    kmeans = KMeans(n_clusters=K, random_state=42, n_init=10)
    kmeans.fit(X_pre)
    labels = kmeans.predict(X_pre)
    joblib.dump(kmeans, KMEANS_PATH)
    print(f"KMeans saved -> {KMEANS_PATH} (k={K})")

    # Attacher labels au dataframe
    df["cluster_label"] = labels

    # PCA pour visualisation
    print("=== Calcul PCA (2D) ===")
    pca = PCA(n_components=2, random_state=42)
    pcs = pca.fit_transform(X_pre)
    # sauvegarder PCA et coordonnées (utile pour Streamlit)
    joblib.dump(pca, PCA_PATH)
    print("PCA model saved ->", PCA_PATH)
    pca_df = pd.DataFrame(pcs, columns=["PC1", "PC2"])
    pca_df["cluster"] = labels
    pca_df.to_csv(PCA_COORDS_CSV, index=False)
    print("PCA coords saved ->", PCA_COORDS_CSV)

    # -------------------------
    # Entraîner un classifieur supervisé pour prédire cluster_label
    # -------------------------
    print("=== Entraînement classifieurs supervisés ===")
    X = X_pre
    y = df["cluster_label"].values

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)

    candidates = {
        "rf": RandomForestClassifier(n_estimators=200, random_state=42, n_jobs=-1),
        "lr": LogisticRegression(max_iter=2000, random_state=42)
    }

    best_name, best_model, best_cv_score = None, None, -1
    for name, model in candidates.items():
        scores = cross_val_score(model, X_train, y_train, cv=5, scoring="accuracy", n_jobs=-1)
        mean_score = float(scores.mean())
        print(f"Model {name} CV accuracy: {mean_score:.4f}")
        if mean_score > best_cv_score:
            best_cv_score = mean_score
            best_name = name
            best_model = model

    # fit best model on full train set
    print(f"Fitting best model: {best_name}")
    best_model.fit(X_train, y_train)
    y_pred = best_model.predict(X_test)
    test_acc = accuracy_score(y_test, y_pred)
    print("Test accuracy:", test_acc)
    print("Classification report:\n", classification_report(y_test, y_pred))

    # Save best classifier
    joblib.dump(best_model, CLASSIFIER_PATH)
    print("Classifier saved ->", CLASSIFIER_PATH)

    # Save metadata
    metadata = {
        "kmeans_k": int(K),
        "classifier": best_name,
        "cv_accuracy": float(best_cv_score),
        "test_accuracy": float(test_acc),
        "created_at": datetime.now().isoformat()
    }
    with open(METADATA_JSON, "w") as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)
    print("Metadata saved ->", METADATA_JSON)

    print("=== FIN du training pipeline ===")

if __name__ == "__main__":
    main()
