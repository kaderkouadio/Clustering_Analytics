"""
sync_all_clusters.py
--------------------
Script utilitaire pour synchroniser les segments clients en base de données.
Récupère les clients sans cluster (ou tous), les envoie à l'API pour prédiction,
et demande à l'API de sauvegarder les résultats.
"""

import requests
import os
import logging
import sys
from datetime import datetime
from pathlib import Path

# --- RÉSOLUTION DES CHEMINS (Indispensable) ---
BASE_DIR = Path(__file__).resolve().parent
if str(BASE_DIR) not in sys.path:
    sys.path.append(str(BASE_DIR))

# Ajout du dossier Backend pour que 'Api.database' soit résolu correctement
BACKEND_PATH = BASE_DIR / "Backend"
if str(BACKEND_PATH) not in sys.path:
    sys.path.append(str(BACKEND_PATH))

# Maintenant, les imports fonctionneront car Python trouvera 'Backend' et 'Api'
try:
    from Backend.Api.database import SessionLocal
    from Backend.Api.models import ClientData
except ImportError:
    # Backup pour certaines configurations d'environnement
    from Backend.Api.database import SessionLocal
    from Backend.Api.models import ClientData

# --- CONFIGURATION DES LOGS (Dossier Logs) ---
LOG_DIR = BASE_DIR / "Logs"
LOG_DIR.mkdir(exist_ok=True)
log_path = LOG_DIR / f"sync_{datetime.now().strftime('%Y-%m-%d')}.log"

# logging.basicConfig(
#     level=logging.INFO,
#     format='%(asctime)s [%(levelname)s] %(message)s',
#     handlers=[logging.FileHandler(log_path, encoding='utf-8'), logging.StreamHandler()]
# )
logger = logging.getLogger("SyncEngine")
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[logging.FileHandler(log_path, encoding='utf-8'), logging.StreamHandler()]
)
# logger = logging.getLogger("SyncEngine")

# def run_global_sync():
#     """
#     Extrait les clients de SQLite, les formate et appelle l'endpoint /cluster
#     pour mettre à jour les étiquettes de segmentation.
#     """
#     logger.info("--- DÉMARRAGE D'UNE NOUVELLE SYNCHRONISATION ---")
#     db = SessionLocal()
#     try:
#         # 1. Extraction des clients (on peut filtrer par ClientData.cluster_kmeans == -1 si besoin)
#         clients_db = db.query(ClientData).all()
        
#         if not clients_db:
#             logger.warning("La base de données est vide. Lancez d'abord ingest_data.py.")
#             return

#         logger.info(f"🔍 {len(clients_db)} clients récupérés pour analyse.")

#         # 2. Préparation du payload JSON (Mapping DB -> ClientSchema)
#         # On inclut l'ID pour permettre à l'API de savoir quel client mettre à jour
#         # payload = {
#         #     "clients": [
#         #         {
#         #             "id": c.id,
#         #             "Age": c.age, 
#         #             "Income": c.income,
#         #             "Education": c.education,
#         #             "Marital_Status": c.marital_status,
#         #             "Customer_Seniority": c.customer_seniority,
#         #             "Kidhome": c.kidhome,
#         #             "Teenhome": c.teenhome,
#         #             "Recency": c.recency,
#         #             "MntWines": c.mnt_wines,
#         #             "MntFruits": c.mnt_fruits,
#         #             "MntMeatProducts": c.mnt_meat,
#         #             "MntFishProducts": c.mnt_fish,
#         #             "MntSweetProducts": c.mnt_sweets,
#         #             "MntGoldProds": c.mnt_gold,
#         #             "NumDealsPurchases": c.num_deals,
#         #             "NumWebPurchases": c.num_web,
#         #             "NumCatalogPurchases": c.num_catalog,
#         #             "NumStorePurchases": c.num_store,
#         #             "NumWebVisitsMonth": c.num_web_visits
#         #         } for c in clients_db
#         #     ]
#         # }


#         # Dans sync_all_clusters.py

#         payload = {
#             "clients": [
#                 {
#                     "id": c.id,
#                     "year_birth": c.year_birth, # Au lieu de "Age" ou "Year_Birth"
#                     "income": c.income,         # Au lieu de "Income"
#                     "education": c.education,
#                     "marital_status": c.marital_status,
#                     "customer_seniority": c.customer_seniority,
#                     "kidhome": c.kidhome,
#                     "teenhome": c.teenhome,
#                     "recency": c.recency,
#                     "mnt_wines": c.mnt_wines,
#                     "mnt_fruits": c.mnt_fruits,
#                     "mnt_meat": c.mnt_meat,
#                     "mnt_fish": c.mnt_fish,
#                     "mnt_sweets": c.mnt_sweets,
#                     "mnt_gold": c.mnt_gold,
#                     "num_deals": c.num_deals,
#                     "num_web": c.num_web,
#                     "num_catalog": c.num_catalog,
#                     "num_store": c.num_store,
#                     "num_web_visits": c.num_web_visits
#                 } for c in clients_db
#             ]
#         }

#         # 3. Appel de l'API avec le flag de sauvegarde
#         url = "http://127.0.0.1:8001/cluster?save_to_db=true"
#         logger.info("📡 Envoi des données à l'API de clustering...")
        
#         response = requests.post(url, json=payload)
        
#         if response.status_code == 200:
#             logger.info("🎉 Succès ! Tous les clients ont été segmentés et mis à jour en base.")
#         else:
#             logger.error(f"❌ Échec de l'API : {response.status_code} - {response.text}")

#     except Exception as e:
#         logger.error(f"❌ Une erreur est survenue lors de la synchronisation : {e}")
#     finally:
#         db.close()
#         logger.info("--- FIN DE SESSION ---")

# if __name__ == "__main__":
#     run_global_sync()






# ... (Gardez vos imports et résolutions de chemins)

def run_global_sync():
    """
    Extrait les clients de SQLite, les formate et appelle l'endpoint /cluster
    pour mettre à jour les étiquettes de segmentation.
    """
    logger.info("--- DÉMARRAGE D'UNE NOUVELLE SYNCHRONISATION ---")
    
    db = SessionLocal()
    try:
        clients_db = db.query(ClientData).all()
        if not clients_db:
            # logger.warning("La base de données est vide.")
            logger.warning("La base de données est vide. Lancez d'abord ingest_data.py.")
            return

        # DEBUG: Vérification du premier ID
        logger.info(f"Premier ID récupéré en base : {clients_db[0].id}")
        logger.info(f"🔍 {len(clients_db)} clients récupérés pour analyse.")

        payload = {
            "clients": [
                {
                    "id": c.id, # On passe l'ID pour que l'API sache qui mettre à jour
                    "Age": c.age, 
                    "Income": c.income,
                    "Education": c.education,
                    "Marital_Status": c.marital_status,
                    "Customer_Seniority": c.customer_seniority,
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
                    "NumWebVisitsMonth": c.num_web_visits
                } for c in clients_db
            ]
        }

        # On force save_to_db=true dans l'URL
        url = "http://127.0.0.1:8001/cluster?save_to_db=true"
        response = requests.post(url, json=payload)
        
        if response.status_code == 200:
            logger.info(f"🎉 Succès ! Réponse API : {response.json().get('status')}")
            logger.info("🎉 Succès ! Tous les clients ont été segmentés et mis à jour en base.")
        else:
            logger.error(f"❌ Échec de l'API : {response.status_code} - {response.text}")

    except Exception as e:
        logger.error(f"❌ Erreur : {e}")
        logger.error(f"❌ Une erreur est survenue lors de la synchronisation : {e}")
    finally:
        db.close()
        logger.info("--- FIN DE SESSION ---")
        # Forcer l'écriture des logs avant de quitter
        for handler in logging.root.handlers:
            handler.close()

if __name__ == "__main__":
    run_global_sync()