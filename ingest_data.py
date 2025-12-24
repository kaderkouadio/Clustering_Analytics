
# import pandas as pd
# import logging
# import os
# import sys
# from pathlib import Path
# from datetime import datetime, timezone

# # --- LOGIQUE DE CHEMINS CRITIQUE ---
# BASE_DIR = Path(__file__).resolve().parent
# # On ajoute la racine et le dossier Backend pour que 'Backend.Api' soit trouvable
# if str(BASE_DIR) not in sys.path:
#     sys.path.append(str(BASE_DIR))

# # On ajoute le dossier Backend pour que l'import 'Api.database' (utilisé dans models.py) fonctionne
# BACKEND_PATH = str(BASE_DIR / "Backend")
# if BACKEND_PATH not in sys.path:
#     sys.path.append(BACKEND_PATH)

# # Maintenant on peut importer
# try:
#     from Backend.Api.database import SessionLocal
#     from Backend.Api.Crud import bulk_upsert_clients
# except ImportError:
#     # Cas de secours si vous avez des imports internes sans le préfixe Backend
#     from Backend.Api.database import SessionLocal
#     from Backend.Api.Crud import bulk_upsert_clients
# # ----------------------------------

# # Configuration des logs
# logging.basicConfig(
#     level=logging.INFO,
#     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
# )
# logger = logging.getLogger("ingestion")

# def clean_marketing_data(file_path: str) -> pd.DataFrame:
#     """Lit et prépare le DataFrame pour la base de données."""
#     if not os.path.exists(file_path):
#         raise FileNotFoundError(f"Le fichier {file_path} est introuvable à la racine.")

#     logger.info(f"📖 Lecture du fichier : {file_path}")
    
#     # Utilisation de sep=None pour détecter automatiquement ',' ou '\t'
#     df = pd.read_csv(file_path, sep=None, engine='python')

#     # 1. Mapping Colonnes CSV -> Modèle SQLAlchemy
#     mapping = {
#         'Year_Birth': 'year_birth',
#         'Education': 'education',
#         'Marital_Status': 'marital_status',
#         'Income': 'income',
#         'Kidhome': 'kidhome',
#         'Teenhome': 'teenhome',
#         'Dt_Customer': 'dt_customer',
#         'Recency': 'recency',
#         'MntWines': 'mnt_wines',
#         'MntFruits': 'mnt_fruits',
#         'MntMeatProducts': 'mnt_meat',
#         'MntFishProducts': 'mnt_fish',
#         'MntSweetProducts': 'mnt_sweets',
#         'MntGoldProds': 'mnt_gold',
#         'NumDealsPurchases': 'num_deals',
#         'NumWebPurchases': 'num_web',
#         'NumCatalogPurchases': 'num_catalog',
#         'NumStorePurchases': 'num_store',
#         'NumWebVisitsMonth': 'num_web_visits'
#     }
#     df = df.rename(columns=mapping)

#     # 2. Nettoyage et Features Engineering
#     df['dt_customer'] = pd.to_datetime(df['dt_customer'], dayfirst=True)
    
#     # Utilisation de timezone.utc pour être moderne
#     now = datetime.now(timezone.utc)
#     current_year = now.year
    
#     df['age'] = current_year - df['year_birth']
#     # Calcul de l'ancienneté (on compare des datetimes naïfs ou aware de façon cohérente)
#     df['customer_seniority'] = ((now.replace(tzinfo=None) - df['dt_customer']).dt.days // 30)

#     # 3. Handling missing values
#     df['income'] = df['income'].fillna(0)

#     # 4. Sélection des colonnes validées dans models.py
#     valid_columns = list(mapping.values()) + ['age', 'customer_seniority']
    
#     return df[valid_columns]

# # def run_ingestion(csv_path: str):
# #     """Exécute le processus complet d'ingestion."""
# #     db = SessionLocal()
# #     try:
# #         df_cleaned = clean_marketing_data(csv_path)
        
# #         logger.info(f"🚀 Injection de {len(df_cleaned)} clients dans SQLite...")
# #         total_inserted = bulk_upsert_clients(db, df_cleaned)
        
# #         logger.info(f"✅ Ingestion terminée : {total_inserted} clients synchronisés.")
        
# #     except Exception as e:
# #         logger.error(f"❌ Erreur lors de l'ingestion : {e}")
# #     finally:
# #         db.close()

# def run_ingestion(csv_path: str):
#     """Exécute le processus complet d'ingestion avec gestion des doublons."""
#     db = SessionLocal()
#     try:
#         df_cleaned = clean_marketing_data(csv_path)
        
#         # On vérifie d'abord combien de lignes on a déjà en base
#         from Backend.Api.models import ClientData
#         existing_count = db.query(ClientData).count()
        
#         logger.info(f"📊 État de la base : {existing_count} clients déjà présents.")
#         logger.info(f"🚀 Préparation de l'analyse de {len(df_cleaned)} lignes du CSV...")

#         # Appel de la fonction de synchronisation
#         # On va modifier bulk_upsert_clients pour qu'elle renvoie le nombre de NOUVEAUX insérés
#         new_inserted, skipped = bulk_upsert_clients(db, df_cleaned)
        
#         if new_inserted == 0 and len(df_cleaned) > 0:
#             logger.info("ℹ️ Toutes les données du fichier existent déjà en base. Aucune modification effectuée.")
#         else:
#             logger.info(f"✅ Ingestion terminée : {new_inserted} nouveaux clients ajoutés, {skipped} doublons ignorés.")
        
#     except Exception as e:
#         logger.error(f"❌ Erreur lors de l'ingestion : {e}")
#         db.rollback()
#     finally:
#         db.close()

# if __name__ == "__main__":
#     # Assurez-vous que ce fichier est bien à la racine avec le script
#     PATH_TO_CSV = "Data/marketing_campaign_clean.csv" 
#     run_ingestion(PATH_TO_CSV)


import pandas as pd
import logging
import os
import sys
from pathlib import Path
from datetime import datetime, timezone

# --- LOGIQUE DE CHEMINS CRITIQUE ---
BASE_DIR = Path(__file__).resolve().parent
if str(BASE_DIR) not in sys.path:
    sys.path.append(str(BASE_DIR))

BACKEND_PATH = str(BASE_DIR / "Backend")
if BACKEND_PATH not in sys.path:
    sys.path.append(BACKEND_PATH)

# --- CONFIGURATION DU DOSSIER LOGS ---
LOG_DIR = BASE_DIR / "Logs"
LOG_DIR.mkdir(exist_ok=True)  # Crée le dossier 'Logs' s'il n'existe pas

# Nom du fichier log (ex: ingestion_2025-12-21.log)
log_filename = f"ingestion_{datetime.now().strftime('%Y-%m-%d')}.log"
log_path = LOG_DIR / log_filename

# Configuration globale du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_path, encoding='utf-8'), # Sauvegarde dans le fichier
        logging.StreamHandler()                          # Affichage dans le terminal
    ]
)
logger = logging.getLogger("ingestion")

# Maintenant on peut importer les modules Backend
try:
    from Backend.Api.database import SessionLocal
    from Backend.Api.Crud import bulk_upsert_clients
except ImportError as e:
    logger.error(f"Erreur d'importation des modules Backend : {e}")
    sys.exit(1)

def clean_marketing_data(file_path: str) -> pd.DataFrame:
    """
    Lit et prépare le DataFrame pour la base de données.
    
    Args:
        file_path (str): Chemin vers le fichier CSV.
    Returns:
        pd.DataFrame: Données nettoyées et prêtes pour l'insertion.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Le fichier {file_path} est introuvable.")

    logger.info(f"📖 Lecture du fichier : {file_path}")
    
    # Détection automatique du séparateur
    df = pd.read_csv(file_path, sep=None, engine='python')

    # 1. Mapping Colonnes CSV -> Modèle SQLAlchemy
    mapping = {
        'Year_Birth': 'year_birth',
        'Education': 'education',
        'Marital_Status': 'marital_status',
        'Income': 'income',
        'Kidhome': 'kidhome',
        'Teenhome': 'teenhome',
        'Dt_Customer': 'dt_customer',
        'Recency': 'recency',
        'MntWines': 'mnt_wines',
        'MntFruits': 'mnt_fruits',
        'MntMeatProducts': 'mnt_meat',
        'MntFishProducts': 'mnt_fish',
        'MntSweetProducts': 'mnt_sweets',
        'MntGoldProds': 'mnt_gold',
        'NumDealsPurchases': 'num_deals',
        'NumWebPurchases': 'num_web',
        'NumCatalogPurchases': 'num_catalog',
        'NumStorePurchases': 'num_store',
        'NumWebVisitsMonth': 'num_web_visits'
    }
    df = df.rename(columns=mapping)

    # 2. Nettoyage et Features Engineering
    df['dt_customer'] = pd.to_datetime(df['dt_customer'], dayfirst=True)
    
    now = datetime.now(timezone.utc)
    current_year = now.year
    
    df['age'] = current_year - df['year_birth']
    # Calcul de l'ancienneté en mois
    df['customer_seniority'] = ((now.replace(tzinfo=None) - df['dt_customer']).dt.days // 30)

    # 3. Gestion des valeurs manquantes
    df['income'] = df['income'].fillna(0)

    # 4. Sélection des colonnes finales
    valid_columns = list(mapping.values()) + ['age', 'customer_seniority']
    
    return df[valid_columns]

def run_ingestion(csv_path: str):
    """
    Exécute le processus complet d'ingestion avec gestion des doublons et logging.
    """
    logger.info("--- DÉMARRAGE DU PROCESSUS D'INGESTION ---")
    db = SessionLocal()
    try:
        df_cleaned = clean_marketing_data(csv_path)
        
        from Backend.Api.models import ClientData
        existing_count = db.query(ClientData).count()
        
        logger.info(f"📊 État de la base : {existing_count} clients déjà présents.")
        logger.info(f"🚀 Analyse de {len(df_cleaned)} lignes du CSV...")

        # Appel de la fonction de synchronisation (retourne un tuple)
        new_inserted, skipped = bulk_upsert_clients(db, df_cleaned)
        
        if new_inserted == 0 and len(df_cleaned) > 0:
            logger.info("ℹ️ Toutes les données existent déjà. Aucune insertion effectuée.")
        else:
            logger.info(f"✅ Ingestion terminée : {new_inserted} nouveaux ajoutés, {skipped} ignorés.")
        
    except Exception as e:
        logger.error(f"❌ Erreur critique lors de l'ingestion : {e}")
        db.rollback()
    finally:
        db.close()
        logger.info("--- FIN DU PROCESSUS ---")

if __name__ == "__main__":
    PATH_TO_CSV = "Data/marketing_campaign_clean.csv" 
    run_ingestion(PATH_TO_CSV)