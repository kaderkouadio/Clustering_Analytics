"""
full_test_db_sqlite.py
----------------------
Script de vérification complet pour la base SQLite :
- Vérification de l'existence du fichier .db
- Inspection des tables et colonnes
- Aperçu des données et comptage
"""

import os
from sqlalchemy import inspect, text
from database import engine, Base, SessionLocal, DB_PATH
# Assurez-vous d'importer vos modèles pour que Base.__subclasses__() fonctionne
from models import ClientData, ClusterProfile, PCAResult 

# -----------------------------
# Test de connexion et Fichier
# -----------------------------
print(f"⏳ Vérification de la base SQLite à l'emplacement : {DB_PATH}")

if not os.path.exists(DB_PATH):
    print("⚠️  Le fichier de base de données n'existe pas encore physiquement.")
else:
    print(f"📂 Fichier détecté ({os.path.getsize(DB_PATH) / 1024:.2f} KB)")

try:
    with engine.connect() as conn:
        # SQLite utilise datetime('now') au lieu de NOW()
        now = conn.execute(text("SELECT datetime('now')")).scalar()
        print(f"✅ Connexion SQLAlchemy OK ! Heure SQLite : {now}")
except Exception as e:
    print("❌ Erreur de connexion :", e)

# -----------------------------
# Inspecteur SQLAlchemy
# -----------------------------
inspector = inspect(engine)
existing_tables = inspector.get_table_names()

print("\n📋 État des tables dans SQLite :")
# On récupère les classes de modèles via Base
for table_class in Base.__subclasses__():
    t_name = table_class.__tablename__
    if t_name in existing_tables:
        print(f"✅ Table '{t_name}' trouvée")
    else:
        print(f"❌ Table '{t_name}' manquante (n'a pas encore été créée)")

# -----------------------------
# Fonction de vérification détaillée
# -----------------------------
def check_table_details(table_class, limit=3):
    t_name = table_class.__tablename__
    if t_name not in existing_tables:
        return

    print(f"\n🔹 Détails de la table : {t_name}")
    
    # Liste des colonnes via l'inspecteur
    columns = [col['name'] for col in inspector.get_columns(t_name)]
    print(f"   Structure : {', '.join(columns)}")

    session = SessionLocal()
    try:
        # Compte total
        total = session.query(table_class).count()
        print(f"   Nombre total de lignes : {total}")

        # Aperçu
        rows = session.query(table_class).limit(limit).all()
        if rows:
            print(f"   Aperçu (top {limit}) :")
            for row in rows:
                # Nettoyage pour l'affichage
                d = {k: v for k, v in row.__dict__.items() if k != "_sa_instance_state"}
                print(f"     - {d}")
    except Exception as e:
        print(f"   ❌ Erreur lors de la lecture des données : {e}")
    finally:
        session.close()

# -----------------------------
# Lancement des tests
# -----------------------------
for table_class in Base.__subclasses__():
    check_table_details(table_class)

print("\n✅ Test SQLite terminé !")