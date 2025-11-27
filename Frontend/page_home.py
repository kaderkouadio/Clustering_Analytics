

# #############################################3

# # Home.py ← FICHIER PRINCIPAL (à la racine)
# import streamlit as st
# from pathlib import Path
# import pandas as pd
# import requests

# # ============================================================
# # CONFIGURATION UNIQUE DE L'APP (doit être en haut !)
# # ============================================================
# st.set_page_config(
#     page_title="Clustering Analytics Dashboard - Kader KOUADIO",
#     page_icon="📊",
#     layout="wide",
#     initial_sidebar_state="expanded"
# )

# # ============================================================
# # TON DESIGN MAGNIFIQUE (inchangé, juste nettoyé)
# # ============================================================
# html_temp = """
#     <div style="
#         background: linear-gradient(90deg, #006400, #228B22); 
#         padding:20px; 
#         border-radius:15px; 
#         box-shadow: 0 6px 16px rgba(0,0,0,0.3);
#         margin-bottom: 20px;
#     ">
#         <h1 style="color: white; text-align:center; font-size: 42px; margin:0;">
#             Dashboard Fullstacks Analytics Pipelines
#         </h1>
#         <p style="color:#e0ffe0; text-align:center; font-size:20px; margin:8px 0 0;">
#             FastAPI + Docker + PostgreSQL + Clustering (KMeans/CAH) + PCA + Streamlit
#         </p>
#     </div>
# """
# st.markdown(html_temp, unsafe_allow_html=True)

# col1, col2, col3 = st.columns([1, 4, 1])
# with col1:
#     st.image("https://raw.githubusercontent.com/kaderkouadio/Fullstacks_Analytics_Pipelines2/main/App_streamlit/Images/profil.jpg", width=100)
# with col2:
#     st.markdown("""
#     <div style="text-align:center; padding:20px; background:#f8fafc; border-radius:12px; box-shadow:0 4px 12px rgba(0,0,0,1.1);">
#         <h2>Segmentation & Recommandation Client Intelligente</h2>
#         <p>Architecture full-stack complète : ML + API + Dashboard + Base de données</p>
#     </div>
#     """, unsafe_allow_html=True)
# with col3:
#     st.markdown("""
#     <div style="text-align:right; padding-top:30px;">
#         <a href="https://www.linkedin.com/in/koukou-kader-kouadio-2a32371a4/" target="_blank">
#             <strong>👨‍💻 KOUADIO KADER</strong>
#         </a>
#     </div>
#     """, unsafe_allow_html=True)

# st.markdown("---")

# # ============================================================
# # PHASE 1 : Pipeline ELT
# # ============================================================
# st.markdown("<h2 style='text-align:center; color:#228B22;'>Phase 1 • Pipeline ELT & Préparation</h2>", unsafe_allow_html=True)
# col1, col2 = st.columns([2, 1])
# with col1:
#     st.image("https://raw.githubusercontent.com/kaderkouadio/Fullstacks_Analytics_Pipelines2/main/App_streamlit/Images/pipeline.png")
# with col2:
#     st.success("**Stockage** : PostgreSQL\n\nTables :\n- `customers`\n- `pca_results`\n- `cluster_profiles`")

# # ============================================================
# # PHASE 2 : Visualisation PCA
# # ============================================================
# st.markdown("<h2 style='text-align:center; color:#228B22;'>Phase 2 • Analyse & Visualisation (PCA)</h2>", unsafe_allow_html=True)
# col1, col2 = st.columns([2, 1])
# with col1:
#     st.image("https://raw.githubusercontent.com/kaderkouadio/Fullstacks_Analytics_Pipelines2/main/App_streamlit/Images/visualisation.jpeg")
# with col2:
#     st.info("**PCA 2D interactif**\n\n4 clusters colorés\n\nProfils moyens par segment")

# # ============================================================
# # PHASE 3 : Modèle & Déploiement
# # ============================================================
# st.markdown("<h2 style='text-align:center; color:#228B22;'>Phase 3 • Modèle & Déploiement</h2>", unsafe_allow_html=True)
# col1, col2 = st.columns([2, 1])
# with col1:
#     st.image("https://raw.githubusercontent.com/kaderkouadio/Fullstacks_Analytics_Pipelines2/main/App_streamlit/Images/streamlit3.jpeg")
# with col2:
#     st.warning("**FastAPI + Docker**\n\nEndpoints :\n/predict-cluster\n/pca\n/health")

# st.markdown("---")

# # ============================================================
# # ÉTAT DES ARTEFACTS (auto-détection propre)
# # ============================================================
# st.markdown("### État des artefacts (Data/)")
# # proc_dir = Path(__file__).parent / "processed_data"
# # Chemin vers ton vrai dossier : Data/ (avec majuscule)
# data_dir = Path(__file__).parent / "Data"
# artifacts = {
#     "preprocessor.joblib": "🧹 Préprocesseur",
#     "kmeans_model.joblib": "🤖 KMeans",
#     "pca_model.joblib": "📉 PCA",
#     "classifier_best.joblib": "🧠 Classifieur",
#     "features_list.json": "📋 Features",
#     "pca_coords.csv": "📊 Coordonnées PCA"
# }

# cols = st.columns(3)
# for i, (file, label) in enumerate(artifacts.items()):
#     with cols[i % 3]:
#         exists = (data_dir / file).exists()
#         st.write(f"**{label}**")
#         st.write("✅ Disponible" if exists else "❌ Manquant")

# if (data_dir / "pca_coords.csv").exists():
#     df = pd.read_csv(data_dir / "pca_coords.csv")
#     st.bar_chart(df["cluster"].value_counts().sort_index())

# # ============================================================
# # TEST API
# # ============================================================
# st.markdown("### Test API FastAPI")
# api_url = st.text_input("URL de base", "http://localhost:8001", label_visibility="collapsed")
# if st.button("Tester /health", use_container_width=True):
#     try:
#         r = requests.get(f"{api_url.rstrip('/')}/health", timeout=5)
#         if r.status_code == 200:
#             st.success("API en ligne !")
#             st.json(r.json())
#         else:
#             st.error(f"Status {r.status_code}")
#     except Exception as e:
#         st.error(f"API hors ligne : {e}")

# # ============================================================
# # INFOS FINALES
# # ============================================================
# st.info("""
# **Prochaines étapes** → Utilise le menu de gauche pour naviguer :
# - Visualisation des clusters
# - Prédiction & recommandations en temps réel
# - Export vers PostgreSQL (bientôt)
# """)

# st.markdown("---")

# # st.markdown("""
# # <div style="text-align:center; padding:30px 20px; background:linear-gradient(135deg, #1e3d59 0%, #2c5364 100%); border-radius:20px; margin:40px 0 20px 0; box-shadow:0 10px 30px rgba(0,0,0,0.3);">
# #     <h2 style="color:#00d4ff; margin:0; font-size:2.2rem; text-shadow:0 0 10px rgba(0,212,255,0.5);">
# #         Koukou Kader KOUADIO
# #         <span style="display:inline-block; margin-left:12px; background:#1DA1F2; color:white; font-size:0.7em; padding:6px 12px; border-radius:50px; vertical-align:middle;">
# #             ✓ Vérifié
# #         </span>
# #     </h2>
    
# #     <p style="color:#a8dadc; margin:15px 0 8px 0; font-size:1.2rem; font-weight:600; letter-spacing:1px;">
# #         Économiste • Analyste Financier • Data Analyst • Développeur BI & Intelligence Artificielle
# #     </p>
    
# #     <p style="color:#e0f7fa; margin:0; font-size:1rem; opacity:0.9;">
# #         © 2025 KOUADIO Kader • Fullstack Data Scientist • 
# #         <span style="color:#ffd700; font-weight:bold;">Projet 100% open-source & production-ready</span>
# #     </p>
# # </div>
# # """, unsafe_allow_html=True)

# # # Option bonus : petit lien discret vers ton GitHub / LinkedIn
# # st.markdown("""
# # <div style="text-align:center; margin-top:15px; font-size:0.9rem; color:#888;">
# #     Made with ❤️ & Streamlit • 
# #     <a href="https://github.com/tonpseudo" target="_blank" style="color:#667eea; text-decoration:none;">GitHub</a> • 
# #     <a href="https://linkedin.com/in/tonprofil" target="_blank" style="color:#667eea; text-decoration:none;">LinkedIn</a>
# # </div>
# # """, unsafe_allow_html=True)

# # st.markdown("---")

# st.markdown("""
# <div style="text-align:center; padding:40px 20px; background:linear-gradient(135deg, #0f2027, #203a43, #2c5364); border-radius:25px; margin:50px 0 20px 0; box-shadow:0 15px 40px rgba(0,0,0,0.4);">
    
#     <h2 style="color:#00e0ff; margin:0; font-size:2.5rem; font-weight:800; letter-spacing:1px;">
#         Koukou Kader KOUADIO 
#         <span style="display:inline-block; margin-left:15px; background:#1DA1F2; color:white; font-size:0.65em; padding:8px 16px; border-radius:50px; vertical-align:middle; box-shadow:0 0 15px rgba(29,161,242,0.6);">
#             Verified
#         </span>
#     </h2>

#     <p style="color:#a8dadc; margin:18px 0 10px 0; font-size:1.25rem; font-weight:600; letter-spacing:1.2px;">
#         Économiste • Analyste Financier • Data Analyst • Développeur BI & Intelligence Artificielle
#     </p>

#     <p style="color:#e0f7fa; margin:10px 0 0 0; font-size:1.05rem; opacity:0.95;">
#         © 2025 KOUADIO Kader • Fullstack Data Scientist • 
#         <span style="color:#ffd700; font-weight:bold; text-shadow:0 0 8px rgba(255,215,0,0.5);">Projet 100% open-source & production-ready</span>
#     </p>

#     <div style="margin-top:20px; font-size:1rem; color:#b0c4de;">
#         Créé avec <span style="color:#ff6b6b; font-weight:bold;">Heart</span> & Streamlit 
#         • <a href="https://github.com/tonpseudo" target="_blank" style="color:#64b5f6; text-decoration:none; font-weight:500;">GitHub</a>
#         • <a href="https://linkedin.com/in/tonprofil" target="_blank" style="color:#64b5f6; text-decoration:none; font-weight:500;">LinkedIn</a>
#     </div>
# </div>
# """, unsafe_allow_html=True)




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
        FastAPI • Docker • PostgreSQL • KMeans/CAH • PCA • Streamlit
    </p>
</div>
""", unsafe_allow_html=True)

# ============================================================
# PROFIL + TITRE
# ============================================================
col1, col2, col3 = st.columns([1.8, 6, 2])

with col1:
    st.image(
        "https://raw.githubusercontent.com/kaderkouadio/Fullstacks_Analytics_Pipelines2/main/App_streamlit/Images/profil.jpg",
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
            <h3 style="margin:0; color:#0077b5;">KOUADIO Kader ✔️</h3>
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
    st.image("https://raw.githubusercontent.com/kaderkouadio/Fullstacks_Analytics_Pipelines2/main/App_streamlit/Images/pipeline.png")

with c2:
    st.success("""
    **Stockage : PostgreSQL**

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
    st.image("https://raw.githubusercontent.com/kaderkouadio/Fullstacks_Analytics_Pipelines2/main/App_streamlit/Images/visualisation.jpeg")

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
    st.image("https://raw.githubusercontent.com/kaderkouadio/Fullstacks_Analytics_Pipelines2/main/App_streamlit/Images/streamlit3.jpeg")

with c2:
    st.warning("""
    **FastAPI + Docker**

    Endpoints de prédiction :
    - `/predict-cluster` : Prédiction du segment client
    - `/pca` : Coordonnées + clusters PCA
    - `/health` : Vérification du statut API
    """)

st.markdown("---")

# # ============================================================
# # ÉTAT DES ARTEFACTS (Auto-détection intelligente)
# # ============================================================
# st.subheader("État des artefacts dans le dossier `Data/`")

# data_dir = Path(__file__).parent.parent / "Data"  # Chemin absolu vers Data/
# artifacts = {
#     "preprocessor.joblib": "Préprocesseur",
#     "kmeans_model.joblib": "Modèle KMeans",
#     "pca_model.joblib": "Modèle PCA",
#     "classifier_best.joblib": "Classifieur",
#     "features_list.json": "Liste des features",
#     "pca_coords.csv": "Coordonnées PCA (affichage)"
# }

# cols = st.columns(3)
# for i, (file, desc) in enumerate(artifacts.items()):
#     path = data_dir / file
#     status = "Disponible" if path.exists() else "Manquant"
#     color = "green" if path.exists() else "red"
#     with cols[i % 3]:
#         st.markdown(f"**{desc}**")
#         st.markdown(f"<span style='color:{color}; font-size:1.3rem;'>→ {status}</span>", unsafe_allow_html=True)

# # Mini aperçu si pca_coords.csv existe
# if (data_dir / "pca_coords.csv").exists():
#     try:
#         df_pca = pd.read_csv(data_dir / "pca_coords.csv")
#         st.success("`pca_coords.csv` chargé avec succès !")
#         col1, col2 = st.columns([1, 2])
#         with col1:
#             st.dataframe(df_pca.head(8), use_container_width=True)
#         with col2:
#             st.bar_chart(df_pca["cluster"].value_counts().sort_index(), use_container_width=True)
#     except Exception as e:
#         st.error(f"Erreur lecture pca_coords.csv : {e}")


# ============================================================
# ÉTAT DES ARTEFACTS (Auto-détection intelligente)
# ============================================================
st.subheader("📦 État des artefacts dans le dossier `Data/`")

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




# ============================================================
# TEST API FASTAPI
# ============================================================
# st.markdown("### Test de l'API FastAPI")
# api_url = st.text_input("URL de l'API", value="http://localhost:8001", label_visibility="collapsed")
# if st.button("Tester /health", type="primary", use_container_width=True):
#     with st.spinner("Connexion en cours..."):
#         try:
#             r = requests.get(f"{api_url.rstrip('/')}/health", timeout=8)
#             if r.status_code == 200:
#                 st.success("API en ligne et fonctionnelle !")
#                 st.json(r.json(), expanded=False)
#             else:
#                 st.error(f"Réponse HTTP {r.status_code}")
#         except Exception as e:
#             st.error(f"Impossible de joindre l'API : {e}")

st.markdown("### Test API FastAPI")
api_url = st.text_input("URL de base", "http://localhost:8001", label_visibility="collapsed")
if st.button("Tester /health", type="primary", use_container_width=True):
    try:
        r = requests.get(f"{api_url.rstrip('/')}/health", timeout=5)
        if r.status_code == 200:
            st.success("API en ligne !")
            st.json(r.json())
        else:
            st.error(f"Status {r.status_code}")
    except Exception as e:
        st.error(f"API hors ligne : {e}")

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
            configure <code>POSTGRES_*</code> et l’URL API dans ton 
            <code>docker-compose.yml</code>.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)


# st.markdown("""
# <div style="text-align:center; margin-top:50px; color:#666; font-size:14px;">
#     © 2025 KOUADIO Kader • Fullstack Data Scientist • Projet complet open-source
# </div>
# """, unsafe_allow_html=True)

# st.markdown("""
# <div style="
#     text-align:center; 
#     margin-top:50px; 
#     color:#555; 
#     font-size:14px;
# ">
#     © 2025 <b>KOUADIO Kader</b> • 
#     <span style="color:#1a73e8; font-weight:bold;">
#         ✔ Vérifié
#     </span>
#     <br>
#     <span style="font-size:15px; color:#333;">
#         Économiste | Analyste Financier | Data Analyst | Développeur BI & Intelligence Artificielle
#     </span>
#     <br>
#     <span style="font-size:13px; color:#777;">Projet complet open-source</span>
# </div>
# """, unsafe_allow_html=True)

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
    <span class="footer-name">KOUADIO Kader</span>
    <span class="footer-badge">✔ Vérifié</span>
    <div class="footer-role">
        Économiste • Analyste Financier • Data Analyst • Développeur BI & Intelligence Artificielle
    </div>
    <div class="footer-sub">© 2025 – Projet complet open-source</div>
</div>
"""

st.markdown(footer_html, unsafe_allow_html=True)

