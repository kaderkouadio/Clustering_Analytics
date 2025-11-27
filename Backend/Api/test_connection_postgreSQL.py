# from database import engine
# from sqlalchemy import text

# try:
#     with engine.connect() as conn:
#         result = conn.execute(text("SELECT NOW()"))
#         print("Connexion OK :", result.scalar())
# except Exception as e:
#     print("Erreur :", e)

"""
test_connection_postgreSQL.py
-----------------------------

Script autonome permettant de tester la connexion à votre base PostgreSQL
via SQLAlchemy.

Ce fichier vérifie :
- L’accès au moteur (engine) défini dans database.py
- La possibilité d’ouvrir une connexion
- La bonne réponse du serveur PostgreSQL à une requête simple (SELECT NOW())

En cas d'erreur :
- Le message affiché aide à diagnostiquer si le problème provient :
    - du serveur PostgreSQL non démarré
    - d’un mauvais mot de passe
    - d’un mauvais port
    - d’une URL SQLAlchemy mal configurée
"""

from database import engine
from sqlalchemy import text

print("⏳ Test de connexion à PostgreSQL...")

try:
    # Tentative de connexion
    with engine.connect() as conn:
        result = conn.execute(text("SELECT NOW()"))
        print("✅ Connexion réussie !")
        print("Horodatage PostgreSQL :", result.scalar())

except Exception as e:
    print("❌ Erreur de connexion :")
    print(e)
    print("\nCauses possibles :")
    print("  - Le service PostgreSQL n'est pas démarré")
    print("  - Mot de passe ou utilisateur incorrect")
    print("  - Mauvais port (5432 ?) ou mauvaise adresse")
    print("  - Problème dans la variable DATABASE_URL dans database.py")

