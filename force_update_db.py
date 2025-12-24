import sys
import os
import joblib
import pandas as pd
import logging
from pathlib import Path
from datetime import datetime

# =========================================================================
# 1. CONFIGURATION DES CHEMINS
# =========================================================================
CURRENT_DIR = Path(__file__).resolve().parent
PROJECT_DIR = CURRENT_DIR 
DATA_DIR = PROJECT_DIR / "Data"

PREPROCESSOR_PATH = DATA_DIR / "preprocessor.joblib"
KMEANS_PATH = DATA_DIR / "kmeans_model.joblib"

sys.path.append(str(PROJECT_DIR))
sys.path.append(str(PROJECT_DIR / "Backend"))

try:
    from Backend.Api.database import SessionLocal
    from Backend.Api.models import ClientData
except ImportError as e:
    print(f"❌ Erreur d'import Backend : {e}")
    sys.exit(1)

# =========================================================================
# 2. CONFIGURATION DES LOGS
# =========================================================================
LOG_DIR = PROJECT_DIR / "Logs"
LOG_DIR.mkdir(exist_ok=True)
log_path = LOG_DIR / f"force_update_{datetime.now().strftime('%Y-%m-%d')}.log"

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[logging.FileHandler(log_path, encoding='utf-8'), logging.StreamHandler()]
)
logger = logging.getLogger("ForceUpdate")

# =========================================================================
# 3. LOGIQUE DE MISE À JOUR
# =========================================================================
def force_sync():
    logger.info("🚀 Démarrage de la mise à jour forcée...")
    
    if not PREPROCESSOR_PATH.exists() or not KMEANS_PATH.exists():
        logger.error(f"❌ Artefacts introuvables dans {DATA_DIR}")
        return

    db = SessionLocal()
    try:
        preprocessor = joblib.load(PREPROCESSOR_PATH)
        kmeans_model = joblib.load(KMEANS_PATH)
        logger.info("📦 Modèles chargés.")
        
        clients = db.query(ClientData).all()
        if not clients:
            logger.warning("Base vide.")
            return
        
        # --- CORRECTION DES COLONNES ---
        # On crée le DataFrame avec les noms EXACTS attendus par le preprocessor
        # Votre modèle a été entraîné avec 'Age' et 'Customer_Seniority' (Majuscules)
        df = pd.DataFrame([{
            "Age": c.age, 
            "Customer_Seniority": c.customer_seniority,
            "Education": c.education, 
            "Marital_Status": c.marital_status,
            "Income": c.income, 
            "Kidhome": c.kidhome, 
            "Teenhome": c.teenhome,
            "Recency": c.recency, 
            "MntWines": c.mnt_wines,
            "MntFruits": c.mnt_fruits, 
            "MntMeatProducts": c.mnt_meat, 
            "MntFishProducts": c.mnt_fish,
            "MntSweetProducts": c.mnt_sweets, 
            "MntGoldProds": c.mnt_gold, 
            "NumDealsPurchases": c.num_deals,
            "NumWebPurchases": c.num_web, 
            "NumCatalogPurchases": c.num_catalog,
            "NumStorePurchases": c.num_store, 
            "NumWebVisitsMonth": c.num_web_visits,
            # Optionnel selon votre pipeline :
            "Year_Birth": 2024 - c.age,
            "Dt_Customer": c.dt_customer
        } for c in clients])

        # Transformation et Prédiction
        # Le preprocessor va maintenant trouver les colonnes 'Age' et 'Customer_Seniority'
        X_transformed = preprocessor.transform(df)
        labels = kmeans_model.predict(X_transformed)

        logger.info(f"💾 Écriture des {len(labels)} clusters dans SQLite...")
        for i, cluster_id in enumerate(labels):
            clients[i].cluster_kmeans = int(cluster_id)
        
        db.commit()
        logger.info("✅ Base de données synchronisée avec succès !")

    except Exception as e:
        logger.error(f"💥 Erreur critique : {str(e)}")
        db.rollback()
    finally:
        db.close()
        logger.info("--- SESSION TERMINÉE ---")

if __name__ == "__main__":
    force_sync()