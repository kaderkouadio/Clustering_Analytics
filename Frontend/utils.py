#####################################################
# utils.py → VERSION FINALE 100% FONCTIONNELLE (Nov 2025)
# Un seul dossier : Data/ (avec majuscule)
# Plus jamais l'erreur "prend 0 argument mais 1 a été donné"
#####################################################

import streamlit as st
from pathlib import Path
import pandas as pd
import joblib
import json
import requests
from typing import Optional, Dict, Any
import os


# -------------------------------------------------------------------------
# UNIQUE DOSSIER : Data/ (majuscule) → tout est là-dedans
# -------------------------------------------------------------------------
def get_data_dir() -> Path:
    """Retourne le chemin vers le dossier Data/ (priorise variable d'environnement)"""
    custom = os.getenv("DATA_DIR")
    if custom:
        return Path(custom).resolve()
    return Path(__file__).resolve().parent.parent / "Data"

# Création automatique si besoin
get_data_dir().mkdir(parents=True, exist_ok=True)


# ============================================================
# CHARGEMENT SÉCURISÉ
# ============================================================
@st.cache_data(show_spinner=False)
def load_csv(path: Path) -> Optional[pd.DataFrame]:
    if not path.exists():
        return None
    try:
        return pd.read_csv(path)
    except Exception as e:
        st.error(f"Erreur CSV {path.name} : {e}")
        return None

@st.cache_resource(show_spinner="Chargement du modèle...")
def load_model(path: Path):
    if not path.exists():
        return None
    try:
        return joblib.load(path)
    except Exception as e:
        st.error(f"Erreur modèle {path.name} : {e}")
        return None

@st.cache_data
def load_json(path: Path) -> Optional[Dict[str, Any]]:
    if not path.exists():
        return None
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        st.warning(f"Erreur JSON {path.name} : {e}")
        return None


# ============================================================
# CHARGEMENT DE TOUS LES ARTEFACTS → FIX DÉFINITIF
# ============================================================
@st.cache_resource(show_spinner="Chargement complet des modèles et données...")
def load_all_artifacts(_hash=None) -> Dict[str, Any]:
    """
    Charge TOUT depuis le dossier Data/
    Le paramètre _hash absorbe l'argument caché de Streamlit → plus jamais l'erreur fatidique
    """
    data_dir = get_data_dir()

    artifacts = {
        "preprocessor":   load_model(data_dir / "preprocessor.joblib"),
        "kmeans":         load_model(data_dir / "kmeans_model.joblib"),
        "pca":            load_model(data_dir / "pca_model.joblib"),
        "classifier":     load_model(data_dir / "classifier_best.joblib"),
        "features":       load_json(data_dir / "features_list.json"),
        "metadata":       load_json(data_dir / "model_metadata.json"),
        "pca_coords":     load_csv(data_dir / "pca_coords.csv"),
        "data_dir":       data_dir,
    }

    return artifacts


# ============================================================
# STATUT DES FICHIERS
# ============================================================
def get_artifacts_status() -> Dict[str, bool]:
    d = get_data_dir()
    return {
        "preprocessor.joblib":    (d / "preprocessor.joblib").exists(),
        "kmeans_model.joblib":    (d / "kmeans_model.joblib").exists(),
        "pca_model.joblib":       (d / "pca_model.joblib").exists(),
        "classifier_best.joblib": (d / "classifier_best.joblib").exists(),
        "features_list.json":     (d / "features_list.json").exists(),
        "model_metadata.json":    (d / "model_metadata.json").exists(),
        "pca_coords.csv":         (d / "pca_coords.csv").exists(),
    }


# ============================================================
# API CLIENT
# ============================================================
@st.cache_data(ttl=3600)
def get_api_url() -> str:
    return os.getenv("FASTAPI_URL", "http://localhost:8001").rstrip("/")

def call_predict_api(payload: Dict[str, Any], endpoint: str = "/predict-cluster", timeout: int = 15):
    url = f"{get_api_url()}{endpoint}"
    try:
        with st.spinner("Prédiction en cours..."):
            r = requests.post(url, json=payload, timeout=timeout)
            r.raise_for_status()
            return r.json()
    except Exception as e:
        st.error(f"Erreur API : {e}")
        if "r" in locals():
            try: st.code(r.text[:1000])
            except: pass
        st.stop()
    return {}


# ============================================================
# UI HELPERS
# ============================================================
def normalize_column_names(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = [c.strip().lower().replace(" ", "_").replace("-", "_") for c in df.columns]
    return df

def show_artifacts_status():
    status = get_artifacts_status()
    cols = st.columns(3)
    for i, (f, ok) in enumerate(status.items()):
        with cols[i % 3]:
            st.write(f"**{f}**")
            if ok:
                st.success("Présent")
            else:
                st.error("Manquant")


# ============================================================
# EXPORT (futur)
# ============================================================
def save_prediction_to_db(*args, **kwargs):
    st.warning("Sauvegarde en base de données : pas encore implémentée")
    return False


