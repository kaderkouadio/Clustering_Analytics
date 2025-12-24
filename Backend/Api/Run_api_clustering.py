
###############################################"

##################################################################################
# ✅ Script Python complet pour automatiser tout le processus Docker
#   ✔️ Compatible Windows
#   ✔️ Affichage propre des logs
##################################################################################
import subprocess
import socket
import time

# ------------------------------
# CONFIGURATION
# ------------------------------
IMAGE_NAME = "img__api_clustering"
CONTAINER_NAME = "api_customer_container"
PORT_HOST = 8001       # port local
PORT_CONTAINER = 80    # port exposé dans le conteneur

# Chemin local vers le dossier Data
DATA_FOLDER = "C:/Users/kkade/Videos/Mes_Applications/Clustering_Analytics/Data"
# Chemin dans le conteneur
CONTAINER_FOLDER = "/Data"

# ------------------------------
# FONCTIONS UTILITAIRES
# ------------------------------
def is_port_in_use(port):
    """Vérifie si un port est déjà utilisé sur localhost"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(("localhost", port)) == 0

def run_command(command, check=True):
    """Exécute une commande shell et affiche stdout/stderr sans planter sur Windows"""
    print(f"👉 {command}")

    result = subprocess.run(
        command,
        shell=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="ignore"
    )

    if result.stdout:
        print(result.stdout)

    if result.stderr and result.returncode != 0:
        print(result.stderr)

    if check and result.returncode != 0:
        raise RuntimeError(f"❌ Erreur lors de : {command}")

    return result

def container_exists(name):
    """Vérifie si le conteneur existe"""
    result = subprocess.run(
        'docker ps -a --format "{{.Names}}"',
        shell=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="ignore"
    )
    return name in result.stdout.strip().splitlines()

def image_exists(name):
    """Vérifie si l’image Docker existe"""
    result = subprocess.run(
        'docker images --format "{{.Repository}}"',
        shell=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="ignore"
    )
    return name in result.stdout.strip().splitlines()

# ------------------------------
# SCRIPT PRINCIPAL
# ------------------------------
def main():
    # Vérifie le port local
    if is_port_in_use(PORT_HOST):
        raise RuntimeError(f"🚫 Le port {PORT_HOST} est déjà utilisé.")

    # # Supprime le conteneur si existant
    # if container_exists(CONTAINER_NAME):
    #     print("🗑 Suppression de l’ancien conteneur...")
    #     run_command(f"docker rm -f {CONTAINER_NAME}")
    if container_exists(CONTAINER_NAME):
        print("🗑 Suppression de l’ancien conteneur...")
        # Ajout de l'arrêt préalable pour une suppression propre
        run_command(f"docker stop {CONTAINER_NAME}", check=False)
        run_command(f"docker rm -f {CONTAINER_NAME}")

    # Supprime l'image précédente si existante
    if image_exists(IMAGE_NAME):
        print("🧹 Suppression de l’image Docker précédente...")
        run_command(f"docker rmi -f {IMAGE_NAME}")

    # Construction de l'image Docker
    print("🔨 Construction de la nouvelle image Docker...")
    run_command(f"docker build -t {IMAGE_NAME} .")

    # Lancement du conteneur avec montage du dossier Data
    print("🚀 Lancement du conteneur...")
    run_command(
        f'docker run -d -p {PORT_HOST}:{PORT_CONTAINER} '
        f'-v "{DATA_FOLDER}:{CONTAINER_FOLDER}" '
        f'--name {CONTAINER_NAME} {IMAGE_NAME}'
    )

    # Attente du démarrage
    print("⏳ Attente du démarrage du conteneur...")
    time.sleep(5)  # peut augmenter si ton API met du temps à démarrer

    # ---------------------------------------------------
    # AFFICHER L’URL AVANT LES LOGS
    # ---------------------------------------------------
    print(f"✅ L'API est accessible sur : http://localhost:{PORT_HOST}/docs")

    # ---------------------------------------------------
    # AFFICHER LES LOGS EN LIVE
    # ---------------------------------------------------
    print(f"📄 Logs du conteneur '{CONTAINER_NAME}': (CTRL+C pour quitter)")

    try:
        run_command(f"docker logs -f {CONTAINER_NAME}", check=False)
    except KeyboardInterrupt:
        print("🛑 Sortie des logs. L'API reste en fonctionnement.")


if __name__ == "__main__":
    main()
