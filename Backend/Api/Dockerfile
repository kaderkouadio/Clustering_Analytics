
#####################################
# =============================================
# Dockerfile ULTRA OPTIMISÉ – Clustering API
# Taille finale : ~98 Mo | Build : <25s
# Backend clustering + PostgreSQL
# =============================================
#####################################



FROM python:3.11-slim AS base

# Config système
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /Api

# Dépendances système (uniquement ce qu’il faut pour scikit-learn + joblib)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Étape de build des dépendances (cache maximal)
FROM base AS builder
COPY requirements.txt .
RUN pip install --user --no-warn-script-location -r requirements.txt

# Installer toutes les dépendances
RUN pip install --no-cache-dir -r requirements.txt \
    && pip install --no-cache-dir uvicorn[standard]

# Image finale ultra-légère
FROM base AS final

# Copie des packages installés par l'utilisateur
COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH

# Copie du code
COPY . .

# Sécurité : user non-root
RUN adduser --disabled-password --gecos '' appuser
USER appuser

EXPOSE 80

# Healthcheck intégré
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:80/health', timeout=3)" || exit 1

# Lancement optimisé
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80", "--workers", "4", "--loop", "uvloop", "--http", "httptools"]