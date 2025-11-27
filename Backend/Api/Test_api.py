
import requests
import json
# ------------------------------
# CONFIGURATION
# ------------------------------
IMAGE_NAME = "img__api_clustering"
CONTAINER_NAME = "api_customer_container"
PORT_HOST = 8001
PORT_CONTAINER = 80

# Chemin local vers le dossier Data
DATA_FOLDER = "C:/Users/kkade/Videos/Mes_Applications/Projet_clustering/Data"
# Chemin dans le conteneur
CONTAINER_FOLDER = "/Data"

BASE_URL = f"http://localhost:{PORT_HOST}"


# ------------------------------
# Payload exemple ClientData
# ------------------------------
client_example_1 = {
    "Age": 45,
    "Customer_Seniority": 36,
    "Income": 45000,
    "Kidhome": 1,
    "Teenhome": 0,
    "Recency": 10,
    "MntWines": 200,
    "MntFruits": 50,
    "MntMeatProducts": 150,
    "MntFishProducts": 30,
    "MntSweetProducts": 20,
    "MntGoldProds": 10,
    "NumDealsPurchases": 3,
    "NumWebPurchases": 15,
    "NumCatalogPurchases": 2,
    "NumStorePurchases": 5,
    "NumWebVisitsMonth": 8,
    "Education": "Graduation",
    "Marital_Status": "Single"
}

client_example_2 = {
    "Age": 30,
    "Customer_Seniority": 12,
    "Income": 30000,
    "Kidhome": 0,
    "Teenhome": 1,
    "Recency": 5,
    "MntWines": 100,
    "MntFruits": 30,
    "MntMeatProducts": 50,
    "MntFishProducts": 10,
    "MntSweetProducts": 5,
    "MntGoldProds": 0,
    "NumDealsPurchases": 1,
    "NumWebPurchases": 5,
    "NumCatalogPurchases": 1,
    "NumStorePurchases": 2,
    "NumWebVisitsMonth": 10,
    "Education": "PhD",
    "Marital_Status": "Married"
}

clients_list = [client_example_1, client_example_2]

# ------------------------------
# 1️⃣ Test /predict-cluster (un client)
# ------------------------------
def test_predict_cluster():
    url = f"{BASE_URL}/predict-cluster"
    payload = client_example_1
    try:
        response = requests.post(url, json=payload, timeout=5)
        response.raise_for_status()
        print("\n✅ /predict-cluster response:")
        print(json.dumps(response.json(), indent=4, ensure_ascii=False))
    except requests.exceptions.RequestException as e:
        print(f"❌ /predict-cluster failed: {e}")


# ------------------------------
# 2. Test /cluster (KMeans non supervisé)
# ------------------------------
def test_cluster():
    url = f"{BASE_URL}/cluster"
    payload = {"clients": clients_list}  # ← CLÉ OBLIGATOIRE grâce à embed=True
    try:
        response = requests.post(url, json=payload, timeout=5)
        response.raise_for_status()
        print("\n/predict-cluster response:")
        print(json.dumps(response.json(), indent=4, ensure_ascii=False))
    except requests.exceptions.RequestException as e:
        print(f"/cluster failed: {e}")
        if hasattr(e.response, "text"):
            print("Détail erreur:", e.response.text)



# ------------------------------
# 3. Test /pca → coordonnées pré-calculées
# ------------------------------
def test_pca_coords():
    url = f"{BASE_URL}/pca"
    try:
        response = requests.get(url, params={"limit": 5}, timeout=10)
        response.raise_for_status()
        print("\n/pca → OK")
        print(json.dumps(response.json(), indent=4, ensure_ascii=False))
    except requests.exceptions.RequestException as e:
        print(f"/pca échoué : {e}")

# ------------------------------
# 4. Test /apply-pca → projection en temps réel
# ------------------------------
def test_apply_pca():
    url = f"{BASE_URL}/apply-pca"
    payload = {"clients": clients_list}  # Même chose ici : {"clients": [...]}
    params = {"n_components": 2}
    try:
        response = requests.post(url, json=payload, params=params, timeout=10)
        response.raise_for_status()
        print("\n/apply-pca → OK")
        print(json.dumps(response.json(), indent=4, ensure_ascii=False))
    except requests.exceptions.RequestException as e:
        print(f"/apply-pca échoué : {e}")
        if hasattr(e.response, "text"):
            print("Détail :", e.response.text)



# ------------------------------
# 5️⃣ Test /segments/stats
# ------------------------------
def test_segment_stats():
    url = f"{BASE_URL}/segments/stats"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        print("\n✅ /segments/stats response:")
        print(json.dumps(response.json(), indent=4, ensure_ascii=False))
    except requests.exceptions.RequestException as e:
        print(f"❌ /segments/stats failed: {e}")

# ------------------------------
# MAIN - Exécuter tous les tests
# ------------------------------
if __name__ == "__main__":
    print("=========================================")
    print("🔹 TEST COMPLET DE L'API FASTAPI 🔹")
    print("=========================================")

    test_predict_cluster()
    test_cluster()
    # test_pca_coords()
    test_apply_pca()
    test_segment_stats()

    print("\n✅ Tous les tests terminés !")
