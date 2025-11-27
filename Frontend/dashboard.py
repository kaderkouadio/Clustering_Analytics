# dashboard.py
###############################################
import os
import sys
import importlib.util
import streamlit as st

# ---------------------------
# Configuration de la page
# ---------------------------
st.set_page_config(
    page_title="Clustering Marketing - Dashboard",
    page_icon="📊",
    layout="wide"
)

# ---------------------------
# Navigation Multi-pages
# ---------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Assure que le dossier courant est dans sys.path pour imports dynamiques
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

# Pages disponibles (fichiers dans ce dossier)
pages = {
    "🏠 Home": "page_home.py",
    "📊 Analyse exploratoire": "page_explore.py",
    "🔎 Prédiction & Recommandations": "page_predict.py"
}

st.sidebar.title("📌 Navigation")
selection = st.sidebar.radio("Aller à :", list(pages.keys()))

module_name = pages[selection]
module_path = os.path.join(BASE_DIR, f"{module_name}")

if os.path.exists(module_path):
    try:
        spec = importlib.util.spec_from_file_location(module_name, module_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
    except Exception as e:
        st.error(f"Erreur lors du chargement de la page `{module_name}` : {e}")
else:
    st.error(f"❌ Fichier {module_path} introuvable")
