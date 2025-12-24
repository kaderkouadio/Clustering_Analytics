
# # =============================================
# # Dockerfile ULTRA OPTIMISÉ – Clustering API
# # Taille finale : ~98 Mo | Build : <25s
# # Backend clustering + SQLite
# # =============================================

FROM python:3.11-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /Backend/Api

# Dépendances système minimales pour scikit-learn
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# --- Stage Builder ---
FROM base AS builder
RUN apt-get update && apt-get install -y --no-install-recommends gcc build-essential
COPY requirements.txt .
# Installation dans /install pour faciliter la copie vers l'image finale
RUN pip install --prefix=/install --no-warn-script-location -r requirements.txt
RUN pip install --prefix=/install uvicorn[standard] httptools uvloop

# --- Stage Final ---
FROM base AS final
# Copie des packages depuis le builder
COPY --from=builder /install /usr/local

# Création du dossier Data pour SQLite (avant le passage en non-root)
RUN mkdir -p /app/Data && chmod 777 /app/Data

# Copie du code source
COPY . .

# Sécurité
RUN adduser --disabled-password --gecos '' appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE 80

# Healthcheck (plus simple pour éviter la dépendance 'requests')
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD python -c "import socket; s = socket.socket(); s.connect(('localhost', 80))" || exit 1

# Lancement (Ajustez le chemin vers main:app selon votre arborescence réelle)
CMD ["uvicorn", "Backend.Api.main:app", "--host", "0.0.0.0", "--port", "80", "--workers", "2"]