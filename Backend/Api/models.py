
"""
models.py
---------
Définition des modèles SQLAlchemy pour Clustering Analytics.
Inclut la documentation des colonnes pour une traçabilité métier totale.
"""

from sqlalchemy import (
    Column, Integer, String, Float, DateTime, JSON, ForeignKey
)
from sqlalchemy.orm import relationship
from datetime import datetime
from datetime import datetime, timezone

# Import de la Base configurée pour SQLite dans database.py
from Api.database import Base

# =====================================================================
#                          Prediction Model
# =====================================================================
class Prediction(Base):
    """
    Stocke les prédictions temps réel effectuées via l'API.
    """
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True)
    payload = Column(JSON, doc="Données d'entrée brutes envoyées à l'API")
    predicted_cluster = Column(Integer, doc="ID du segment prédit par le modèle RandomForest")
    confidence = Column(Float, doc="Score de probabilité (0 à 1) du classifieur")
    # timestamp = Column(DateTime, default=datetime.utcnow, doc="Date et heure de la prédiction")
    # Correction ici : Utilisation de la méthode moderne recommandée
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    pc1 = Column(Float, nullable=True, doc="Coordonnée sur le premier axe principal PCA")
    pc2 = Column(Float, nullable=True, doc="Coordonnée sur le second axe principal PCA")


# =====================================================================
#                          ClientData Model
# =====================================================================
class ClientData(Base):
    """
    Modèle représentant un client dans le dataset marketing historique.
    """
    __tablename__ = "client_data"

    id = Column(Integer, primary_key=True, autoincrement=True)

    # ---- Données démographiques ----
    year_birth = Column(Integer, doc="Année de naissance du client")
    education = Column(String, doc="Niveau d'éducation du client")
    marital_status = Column(String, doc="Statut marital du client")
    income = Column(Float, doc="Revenu annuel du client")

    # ---- Informations temporelles ----
    dt_customer = Column(DateTime, doc="Date d'inscription du client dans la base")
    age = Column(Integer, doc="Âge calculé au moment de l'analyse")
    customer_seniority = Column(Integer, doc="Ancienneté du client en mois")

    # ---- Vie de famille & Interaction ----
    kidhome = Column(Integer, doc="Nombre d'enfants (0-12 ans) au foyer")
    teenhome = Column(Integer, doc="Nombre d'adolescents (13-17 ans) au foyer")
    recency = Column(Integer, doc="Nombre de jours depuis le dernier achat")

    # ---- Dépenses (Mnt) ----
    mnt_wines = Column(Float, doc="Montant dépensé en vins sur 2 ans")
    mnt_fruits = Column(Float, doc="Montant dépensé en fruits sur 2 ans")
    mnt_meat = Column(Float, doc="Montant dépensé en viandes sur 2 ans")
    mnt_fish = Column(Float, doc="Montant dépensé en poissons sur 2 ans")
    mnt_sweets = Column(Float, doc="Montant dépensé en confiseries sur 2 ans")
    mnt_gold = Column(Float, doc="Montant dépensé en produits de luxe sur 2 ans")

    # ---- Canaux d'achat ----
    num_deals = Column(Integer, doc="Nombre d'achats effectués avec une réduction")
    num_web = Column(Integer, doc="Nombre d'achats effectués via le site web")
    num_catalog = Column(Integer, doc="Nombre d'achats effectués via catalogue")
    num_store = Column(Integer, doc="Nombre d'achats effectués en magasin physique")
    num_web_visits = Column(Integer, doc="Nombre de visites sur le site web par mois")

    # ---- Résultats de clustering ----
    cluster_kmeans = Column(Integer, nullable=True, doc="Cluster attribué par l'algorithme K-Means")
    cluster_cah = Column(Integer, nullable=True, doc="Cluster attribué par la Classification Ascendante Hiérarchique")

    # Relation vers les résultats PCA
    pca_results = relationship("PCAResult", back_populates="customer", cascade="all, delete-orphan")


# =====================================================================
#                        ClusterProfile Model
# =====================================================================
class ClusterProfile(Base):
    """
    Contient les statistiques agrégées pour chaque segment marketing.
    """
    __tablename__ = "cluster_profiles"

    id = Column(Integer, primary_key=True, autoincrement=True)
    model_type = Column(String, doc="Type de modèle source (ex: kmeans)")
    cluster_label = Column(Integer, doc="Identifiant du segment (0, 1, 2, 3)")
    profile_data = Column(JSON, doc="Dictionnaire JSON des moyennes et KPIs du segment")
    # created_at = Column(DateTime, default=datetime.utcnow, doc="Date de création du profil")
    # Correction ici aussi
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


# =====================================================================
#                          PCAResult Model
# =====================================================================
class PCAResult(Base):
    """
    Coordonnées PCA d'un client pour la visualisation 2D.
    """
    __tablename__ = "pca_results"

    id = Column(Integer, primary_key=True, autoincrement=True)
    client_id = Column(Integer, ForeignKey("client_data.id"), doc="Référence vers le client")

    pc1 = Column(Float, doc="Première composante principale")
    pc2 = Column(Float, doc="Deuxième composante principale")
    model_type = Column(String, default="kmeans", doc="Modèle utilisé pour la projection")
    # created_at = Column(DateTime, default=datetime.utcnow)
    # Correction ici aussi
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    # Relation inverse vers ClientData
    customer = relationship("ClientData", back_populates="pca_results")