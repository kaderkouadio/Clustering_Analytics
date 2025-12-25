
# Home.py → Page d'accueil principale
import streamlit as st
from pathlib import Path
import pandas as pd
import requests

# ============================================================
# CONFIGURATION DE LA PAGE
# ============================================================
st.set_page_config(
    page_title="Clustering Analytics Dashboard - Kader KOUADIO",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# HEADER MAGNIFIQUE
# ============================================================
st.markdown("""
<div style="
    background: linear-gradient(90deg, #006400, #228B22, #32CD32);
    padding: 30px;
    border-radius: 20px;
    text-align: center;
    box-shadow: 0 10px 30px rgba(0,0,0,0.3);
    margin-bottom: 30px;
">
    <h1 style="color:white; margin:0; font-size:3.2rem; font-weight:800;">
        Dashboard Fullstack Analytics Pipelines
    </h1>
    <p style="color:#e8f5e8; font-size:1.4rem; margin:10px 0 0;">
        FastAPI • Docker • SQLite • KMeans/CAH • PCA • Streamlit
    </p>
</div>
""", unsafe_allow_html=True)

# ============================================================
# PROFIL + TITRE
# ============================================================
col1, col2, col3 = st.columns([1.8, 6, 2])

with col1:
    st.image(
        "https://raw.githubusercontent.com/kaderkouadio/Clustering_Analytics/main/Frontend/Images/profil.jpg",
        # "https://raw.githubusercontent.com/kaderkouadio/Projet_clustering/Frontend/Images/profil.jpg",
        width=140,
        caption="Koukou Kader KOUADIO"
    )

with col2:
    st.markdown("""
    <div style="
        background:#f8f9fa;
        padding:25px;
        border-radius:15px;
        text-align:center;
        box-shadow:0 6px 20px rgba(0,0,0,0.1);
    ">
        <h2 style="margin:0; color:#1e40af;">Segmentation & Recommandation Client Intelligente</h2>
        <p style="font-size:1.15rem; color:#444; margin-top:8px;">
            Architecture full-stack complète • Machine Learning • API REST • Dashboard interactif
        </p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div style="text-align:right; padding-top:20px;">
        <a href="https://www.linkedin.com/in/koukou-kader-kouadio-2a32371a4/" target="_blank" style="text-decoration:none;">
            <h3 style="margin:0; color:#0077b5;"> KOUADIO Kader ✔️</h3>
            <p style="margin:5px 0 0; color:#0a66c2; font-weight:bold;">Voir profil LinkedIn →</p>
        </a>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ============================================================
# PHASE 1 - Pipeline ELT
# ============================================================
st.markdown("<h2 style='text-align:center; color:#228B22;'>Phase 1 • Pipeline ELT & Préparation</h2>", unsafe_allow_html=True)

c1, c2 = st.columns([2.2, 1])
with c1:

    st.image("https://raw.githubusercontent.com/kaderkouadio/Clustering_Analytics/main/Frontend/Images/Pipelines.png", width=600)


with c2:
    st.success("""
    **Stockage : SQLite**

    Tables créées automatiquement :
    - `customers`
    - `pca_results`
    - `cluster_profiles`
    """)

# ============================================================
# PHASE 2 - Visualisation PCA
# ============================================================
st.markdown("<h2 style='text-align:center; color:#228B22;'>Phase 2 • Analyse & Visualisation PCA</h2>", unsafe_allow_html=True)

c1, c2 = st.columns([2.2, 1])
with c1:

    st.image("https://raw.githubusercontent.com/kaderkouadio/Clustering_Analytics/main/Frontend/Images/Dataviz2.jpg", width=600)

with c2:
    st.info("""
    **Fonctionnalités :**
    - Nuage de points PCA 2D interactif
    - 4 segments clients colorés
    - Profils sociodémographiques par cluster
    """)

# ============================================================
# PHASE 3 - Modèle & Déploiement
# ============================================================
st.markdown("<h2 style='text-align:center; color:#228B22;'>Phase 3 • Modèle & Déploiement</h2>", unsafe_allow_html=True)

c1, c2 = st.columns([2.2, 1])
with c1:

    st.image("https://raw.githubusercontent.com/kaderkouadio/Clustering_Analytics/main/Frontend/Images/Deployment.jpg", width=600)

with c2:
    st.warning("""
    **FastAPI + Docker**

    Endpoints de prédiction :
    - `/predict-cluster` : Prédiction du segment client
    - `/pca` : Coordonnées + clusters PCA
    - `/health` : Vérification du statut API
    """)

st.markdown("---")

# ============================================================
# ÉTAT DES ARTEFACTS (Auto-détection intelligente)
# ============================================================
st.subheader("📦 État des artefacts ")

data_dir = Path(__file__).parent.parent / "Data"  # Chemin absolu vers Data/
artifacts = {
    "preprocessor.joblib": "Préprocesseur",
    "kmeans_model.joblib": "Modèle KMeans",
    "pca_model.joblib": "Modèle PCA",
    "classifier_best.joblib": "Classifieur",
    "features_list.json": "Liste des features",
    "pca_coords.csv": "Coordonnées PCA (affichage)"
}

# --- Carte de résumé
with st.container():
    st.markdown(
        """
        <div style='padding:12px; background:#f7f7f7; border-left:6px solid #2196F3; border-radius:6px; margin-bottom:15px;'>
            🔍 <strong>Astuce :</strong> Tous les artefacts doivent être présents pour activer la prédiction et la
            visualisation PCA. Vérifiez ci-dessous l’état de chaque fichier.
        </div>
        """,
        unsafe_allow_html=True
    )

# --- Affichage des artefacts
cols = st.columns(3)
for i, (file, label) in enumerate(artifacts.items()):
    file_path = data_dir / file
    exists = file_path.exists()

    color = "green" if exists else "red"
    status = "✔️ Disponible" if exists else "❌ Manquant"

    with cols[i % 3]:
        st.markdown(f"### {label}")
        st.markdown(
            f"<p style='color:{color}; font-size:1.2rem; font-weight:bold;'>{status}</p>",
            unsafe_allow_html=True
        )
        st.markdown(
            f"<span style='font-size:11px; color:#777;'>({file})</span>",
            unsafe_allow_html=True
        )

st.markdown("---")

# --- Aperçu du fichier PCA si disponible
pca_path = data_dir / "pca_coords.csv"

if pca_path.exists():
    try:
        df_pca = pd.read_csv(pca_path)
        st.success("`pca_coords.csv` chargé avec succès 🎉")

        col1, col2 = st.columns([1, 2])

        with col1:
            st.markdown("#### Aperçu des données PCA")
            st.dataframe(df_pca.head(8), use_container_width=True)

        with col2:
            st.markdown("#### Distribution des clusters")
            st.bar_chart(
                df_pca["cluster"].value_counts().sort_index(),
                use_container_width=True
            )

    except Exception as e:
        st.error(f"Impossible de lire `pca_coords.csv` : {e}")

else:
    st.info("📁 Aucun aperçu PCA disponible — fichier `pca_coords.csv` manquant.")


# st.markdown("### Test API FastAPI")
# import requests
# import streamlit as st

# # ... votre code précédent ...

# api_url= "https://clustering-analytics.onrender.com"

# if st.button("Vérifier la connexion à l'API"):
#     try:
#         response = requests.get(f"{api_url}/") # Teste la racine ou /docs
#         if response.status_code == 200:
#             st.success("API en ligne !")
#         else:
#             st.warning(f"L'API répond avec le code : {response.status_code}")
#     except:
#         st.error("L'API est en cours de réveil ou inaccessible. Attendez 30 secondes et réessayez.")
# api_url = st.text_input("URL de base", "https://clustering-analytics.onrender.com", label_visibility="collapsed")
# if st.button("Tester /health", type="primary", use_container_width=True):
#     try:
#         r = requests.get(f"{api_url.rstrip('/')}/health", timeout=5)
#         if r.status_code == 200:
#             st.success("API en ligne !")
#             st.json(r.json())
#         else:
#             st.error(f"Status {r.status_code}")
#     except Exception as e:
#         st.error(f"API hors ligne : {e}")
st.markdown("### 🛠 Diagnostic de Connexion")

# Utilisation d'une fonction pour centraliser les appels
def check_api(url, endpoint):
    target = f"{url.rstrip('/')}/{endpoint.lstrip('/')}"
    try:
        r = requests.get(target, timeout=10)
        return r
    except Exception as e:
        return str(e)

api_url = st.text_input("URL de l'API", value="https://clustering-analytics.onrender.com")

col1, col2 = st.columns(2)

with col1:
    if st.button("🚀 Lancer le Diagnostic"):
        res = check_api(api_url, "/health")
        if isinstance(res, requests.Response) and res.status_code == 200:
            data = res.json()
            if data.get("status") == "Online":
                st.success(f"✅ {data.get('message')}")
                # Affiche l'état des artefacts en colonnes compactes
                st.write("**État des composants :**")
                st.json(data.get("artifacts"))
            else:
                st.warning("⚠️ API en ligne mais en mode dégradé.")
        else:
            st.error("❌ API injoignable. (Vérifiez le déploiement Render)")

with col2:
    res = check_api(api_url, "/health")
    if isinstance(res, requests.Response) and res.status_code == 200:
        data = res.json()
        st.success("API en ligne")
        
        # Affichage élégant des composants
        arts = data.get("artifacts", {})
        cols = st.columns(len(arts))
        for i, (name, status) in enumerate(arts.items()):
            cols[i].metric(label=name.capitalize(), value="✅" if status else "❌")
    else:
        st.error("L'API ne répond pas")
# ============================================================
# NAVIGATION
# ============================================================
st.markdown("---")
st.markdown("## 🚀 Navigation dans l'application")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(
        """
        <div style='padding:15px; background-color:#f1f8ff; border-radius:10px; 
                    border-left:5px solid #2196F3; transition:0.3s;'>
            <h4 style='margin-bottom:5px;'>📊 Visualisation des Clusters</h4>
            <p style='font-size:14px; color:#444;'>Nuage PCA + Profils détaillés</p>
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        """
        <div style='padding:15px; background-color:#f1f8ff; border-radius:10px; 
                    border-left:5px solid #4CAF50; transition:0.3s;'>
            <h4 style='margin-bottom:5px;'>🤖 Prédiction en temps réel</h4>
            <p style='font-size:14px; color:#444;'>Saisie des données → Segment instantané</p>
        </div>
        """,
        unsafe_allow_html=True
    )

with col3:
    st.markdown(
        """
        <div style='padding:15px; background-color:#f1f8ff; border-radius:10px; 
                    border-left:5px solid #FF9800; transition:0.3s;'>
            <h4 style='margin-bottom:5px;'>🗄️ Exploration libre</h4>
            <p style='font-size:14px; color:#444;'>Téléverse ton fichier et analyse-le</p>
        </div>
        """,
        unsafe_allow_html=True
    )



# ------------------------------------------------------------
# Boîte d'information (identique style)
# ------------------------------------------------------------
st.markdown(
    """
    <div style='
        margin-top: 30px;
        background-color: #e8f4fd;
        border-left: 5px solid #2196F3;
        padding: 15px 20px;
        border-radius: 5px;
        font-size: 16px;
        color: #333;
    '>
        <p>
            ℹ️ <strong>Note Render :</strong> L’API hébergée sur 
            <strong>Render</strong> peut mettre quelques secondes à démarrer si elle est en veille.
        </p>
        <p>
            ℹ️ <strong>Note Artefacts :</strong> Place tes fichiers 
            <code>.joblib</code> et <code>.json</code> dans le dossier 
            <strong>Data/</strong> à la racine du projet.
        </p>
        <p>
            ℹ️ <strong>Note Docker :</strong> Si tu utilises Docker, 
            configure <code>SQLite*</code> et l’URL API dans ton 
            <code>docker-compose.yml</code>.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown("---")

footer_html = """
<style>
.footer-container {
    text-align:center;
    margin-top:40px;
    padding:20px 10px;
    color:#4a4a4a;
    font-family: 'Segoe UI', sans-serif;
}

.footer-name {
    font-size:22px;
    font-weight:700;
    color:#222;
}

.footer-badge {
    display:inline-block;
    background:#1a73e8;
    color:white;
    padding:3px 10px;
    border-radius:12px;
    font-size:13px;
    margin-left:8px;
    font-weight:600;
}

.footer-role {
    font-size:15px;
    margin-top:6px;
    color:#333;
}

.footer-sub {
    font-size:13px;
    margin-top:4px;
    color:#777;
}
</style>

<div class="footer-container">
    <span class="footer-name"> KOUADIO Kader</span>
    <span class="footer-badge">✔ Vérifié</span>
    <div class="footer-role">
        Économiste • Analyste Financier • Data Analyst • Développeur BI & Intelligence Artificielle
    </div>
    <div class="footer-sub">© 2025 – Projet complet open-source</div>
</div>
"""

st.markdown(footer_html, unsafe_allow_html=True)