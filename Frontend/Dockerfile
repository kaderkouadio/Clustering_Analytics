# FROM python:3.11-slim

# WORKDIR /app

# COPY ./app /app

# RUN pip install --no-cache-dir -r requirements.txt

# CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]



# Utilisation d'une image légère et stable
FROM python:3.11-slim

# Éviter que Python ne génère des fichiers .pyc et forcer l'affichage des logs en temps réel
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Installation des dépendances système nécessaires pour certaines bibliothèques ML ou SQL
# (Libpq-dev est souvent nécessaire si vous utilisez PostgreSQL avec psycopg2)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copier d'abord le requirements pour profiter du cache des layers Docker
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copier le reste de l'application et le dossier Data/
COPY . .

# Exposer le port par défaut de Streamlit
EXPOSE 8501

# Santé de l'application (Healthcheck)
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# Lancement de Streamlit
CMD ["streamlit", "run", "Home.py", "--server.port=8501", "--server.address=0.0.0.0"]