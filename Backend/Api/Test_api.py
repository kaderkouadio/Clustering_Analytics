# ============================================================
# Test_api.py 
# 
# ============================================================

import requests
import json
import time
from datetime import datetime




# -------------------------------------------------------------------------
# CONFIGURATION ET SETUP
# -------------------------------------------------------------------------
IMAGE_NAME = "img__api_clustering"
CONTAINER_NAME = "api_customer_container"
PORT_HOST = 8001
PORT_CONTAINER = 80
# BASE_URL = f"http://localhost:{PORT_HOST}"
BASE_URL = f"http://127.0.0.1:{PORT_HOST}"

# Couleurs pour la console
GREEN = "\033[92m"
RED = "\033[91m"
BLUE = "\033[94m"
ENDC = "\033[0m"

# Chemin local vers le dossier Data
DATA_FOLDER = "C:/Users/kkade/Videos/Mes_Applications/Projet_clustering/Data"
# Chemin dans le conteneur
CONTAINER_FOLDER = "/Data"



# -------------------------------------------------------------------------
# JEUX DE DONNÉES DE TEST
# -------------------------------------------------------------------------
client_vip = {
    "Age": 45, "Customer_Seniority": 36, "Income": 85000,
    "Kidhome": 0, "Teenhome": 0, "Recency": 10,
    "MntWines": 800, "MntFruits": 150, "MntMeatProducts": 500,
    "MntFishProducts": 130, "MntSweetProducts": 120, "MntGoldProds": 100,
    "NumDealsPurchases": 1, "NumWebPurchases": 10, "NumCatalogPurchases": 8,
    "NumStorePurchases": 10, "NumWebVisitsMonth": 2,
    "Education": "PhD", "Marital_Status": "Married"
}

client_standard = {
    "Age": 30, "Customer_Seniority": 12, "Income": 30000,
    "Kidhome": 1, "Teenhome": 0, "Recency": 45,
    "MntWines": 50, "MntFruits": 10, "MntMeatProducts": 20,
    "MntFishProducts": 5, "MntSweetProducts": 5, "MntGoldProds": 5,
    "NumDealsPurchases": 5, "NumWebPurchases": 2, "NumCatalogPurchases": 0,
    "NumStorePurchases": 3, "NumWebVisitsMonth": 8,
    "Education": "Graduation", "Marital_Status": "Single"
}

# -------------------------------------------------------------------------
# FONCTIONS DE TEST
# -------------------------------------------------------------------------

def run_test(name, func):
    print(f"\n{BLUE}--- Test: {name} ---{ENDC}")
    start = time.time()
    try:
        func()
        elapsed = time.time() - start
        print(f"{GREEN}✅ Réussi ({elapsed:.3f}s){ENDC}")
    except Exception as e:
        print(f"{RED}❌ Échec: {e}{ENDC}")

def test_health_and_db():
    # Test Health
    r = requests.get(f"{BASE_URL}/health")
    r.raise_for_status()
    print("Health:", r.json()["status"])
    
    # Test SQLite Connection
    r = requests.get(f"{BASE_URL}/test-db")
    r.raise_for_status()
    print("DB Status:", r.json()["connection"])
    print("Tables:", r.json()["tables"])

def test_predict_single():
    url = f"{BASE_URL}/predict-cluster"
    response = requests.post(url, json=client_vip)
    response.raise_for_status()
    data = response.json()
    print(f"Cluster prédit: {data['cluster']} (Probabilité: {data.get('probability', 'N/A')})")

def test_batch_clustering():
    url = f"{BASE_URL}/cluster"
    # Note: embed=True impose d'envelopper la liste dans une clé "clients"
    payload = {"clients": [client_vip, client_standard]}
    response = requests.post(url, json=payload)
    response.raise_for_status()
    results = response.json()["results"]
    for res in results:
        print(f"Client {res['client_index']}: Segment '{res['segment']}' | Priorité: {res['priority']}")

def test_pca_projection():
    url = f"{BASE_URL}/apply-pca"
    payload = {"clients": [client_vip, client_standard]}
    params = {"n_components": 2}
    response = requests.post(url, json=payload, params=params)
    response.raise_for_status()
    coords = response.json()["pca_components"]
    print(f"Coordonnées PCA (Client 1): {coords[0]}")

def test_save_to_sqlite():
    url = f"{BASE_URL}/save-prediction"
    # Simulation d'un retour de prédiction complet pour sauvegarde
    payload = {
        "payload": client_vip,
        "predicted_cluster": 0,
        "confidence": 0.99,
        "pc1": 2.45,
        "pc2": -1.12
    }
    response = requests.post(url, json=payload)
    response.raise_for_status()
    print(f"ID Enregistrement SQLite: {response.json().get('id')}")

def test_stats():
    url = f"{BASE_URL}/segments/stats"
    response = requests.get(url)
    response.raise_for_status()
    print("Aperçu Stats:", response.json()["data"][:2])

# -------------------------------------------------------------------------
# EXECUTION
# -------------------------------------------------------------------------
if __name__ == "__main__":
    print(f"{BLUE}=========================================")
    print("🚀 DÉMARRAGE DES TESTS API CLUSTERING")
    print(f"URL: {BASE_URL}")
    print(f"========================================={ENDC}")

    run_test("Santé & Base SQLite", test_health_and_db)
    run_test("Prédiction Individuelle", test_predict_single)
    run_test("Clustering par Lot (Batch)", test_batch_clustering)
    run_test("Projection PCA temps réel", test_pca_projection)
    run_test("Sauvegarde en Base de Données", test_save_to_sqlite)
    run_test("Statistiques des Segments", test_stats)

    print(f"\n{GREEN}✨ Tous les tests critiques sont terminés !{ENDC}")