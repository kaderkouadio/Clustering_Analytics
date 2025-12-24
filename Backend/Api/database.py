# ============================================================
# database.py - Projet Clustering Analytics
# Gestion de la persistance des données avec SQLite
# ============================================================

import logging
import os
from pathlib import Path
from sqlalchemy import create_engine, inspect, text, Column, Integer, Float, String
from sqlalchemy.orm import declarative_base, sessionmaker

# ------------------------------------------------------------
# 1. Configuration des Logs
# ------------------------------------------------------------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("database")

# ------------------------------------------------------------
# 2. Configuration SQLite
# ------------------------------------------------------------
DB_FILE = "clustering_analytics.db"
# Utilisation de Path pour une gestion propre des chemins (Windows/Linux)
DB_PATH = Path(__file__).parent / DB_FILE
DATABASE_URL = f"sqlite:///{DB_PATH}"

# Vérification/Création du fichier physique
if DB_PATH.exists():
    logger.info(f"✔️ Base SQLite détectée : {DB_PATH}")
else:
    logger.info(f"📌 Initialisation d'une nouvelle base SQLite : {DB_PATH}")

# ------------------------------------------------------------
# 3. Moteur & Session SQLAlchemy
# ------------------------------------------------------------
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}, # Requis pour SQLite + FastAPI
    echo=False,
    future=True
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
    future=True
)

Base = declarative_base()

# ------------------------------------------------------------
# 4. Modèle Client (Table Principale)
# ------------------------------------------------------------
class Client(Base):
    __tablename__ = "clients"
    
    id = Column(Integer, primary_key=True, index=True)
    Age = Column(Float, nullable=False)
    Customer_Seniority = Column(Float, nullable=False)
    Income = Column(Float, nullable=False)
    Kidhome = Column(Integer, nullable=False)
    Teenhome = Column(Integer, nullable=False)
    Recency = Column(Integer, nullable=False)
    MntWines = Column(Float, nullable=False)
    MntFruits = Column(Float, nullable=False)
    MntMeatProducts = Column(Float, nullable=False)
    MntFishProducts = Column(Float, nullable=False)
    MntSweetProducts = Column(Float, nullable=False)
    MntGoldProds = Column(Float, nullable=False)
    NumDealsPurchases = Column(Integer, nullable=False)
    NumWebPurchases = Column(Integer, nullable=False)
    NumCatalogPurchases = Column(Integer, nullable=False)
    NumStorePurchases = Column(Integer, nullable=False)
    NumWebVisitsMonth = Column(Integer, nullable=False)
    Education = Column(String, nullable=True)
    Marital_Status = Column(String, nullable=True)
    cluster = Column(Integer, nullable=True)

# ------------------------------------------------------------
# 5. Initialisation Automatique du Schéma
# ------------------------------------------------------------
def create_tables():
    """Crée les tables avec un monitoring détaillé dans les logs."""
    inspector = inspect(engine)
    existing_tables = inspector.get_table_names()
    
    # Création des tables manquantes
    Base.metadata.create_all(bind=engine)
    
    declared_tables = Base.metadata.tables.keys()
    for table in declared_tables:
        if table in existing_tables:
            logger.info(f"✔️ Table opérationnelle : {table}")
        else:
            logger.info(f"🆕 Table créée avec succès : {table}")

# ------------------------------------------------------------
# 6. Dépendance FastAPI
# ------------------------------------------------------------
def get_db():
    """Générateur de session pour les endpoints de l'API."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Initialisation au chargement du module
if __name__ == "database" or __name__ == "__main__":
    create_tables()

# ------------------------------------------------------------
# 7. Test de Connexion (Exécution directe)
# ------------------------------------------------------------
if __name__ == "__main__":
    try:
        with engine.connect() as conn:
            version = conn.execute(text("SELECT sqlite_version()")).scalar()
            logger.info(f"🚀 Test réussi ! SQLite version : {version}")
    except Exception as e:
        logger.error(f"❌ Échec de connexion : {e}")