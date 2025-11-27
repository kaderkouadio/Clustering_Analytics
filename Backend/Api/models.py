"""
models.py
---------

Contient la définition des modèles SQLAlchemy utilisés dans le projet
de segmentation et d'analyse des clients. Les modèles suivants sont inclus :

- Customer : Représente un client individuel, avec ses informations démographiques,
             comportementales et les résultats de clustering.
- ClusterProfile : Représente un profil statistique associé à un cluster donné.
- PCAResult : Stocke les coordonnées PCA d'un client pour représentation graphique.

Chaque modèle est accompagné de commentaires explicatifs pour une compréhension claire.
"""

from sqlalchemy import Column, Integer, String, Float, DateTime, JSON, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime

Base = declarative_base()


# =====================================================================
#                           Customer Model
# =====================================================================
class Customer(Base):
    """
    Modèle représentant un client.

    Contient :
    - Données démographiques (âge, revenu, statut marital, etc.)
    - Comportements d’achat (dépenses par catégorie)
    - Données de relation client (ancienneté, fréquentation)
    - Résultats de clustering (KMeans, CAH)
    """

    __tablename__ = "customers"

    # ---- Identifiant principal ----
    id = Column(Integer, primary_key=True, autoincrement=True)

    # ---- Données démographiques ----
    year_birth = Column(Integer, doc="Année de naissance du client")
    education = Column(String, doc="Niveau d'éducation du client")
    marital_status = Column(String, doc="Statut marital du client")
    income = Column(Float, doc="Revenu annuel du client")

    # ---- Informations générales ----
    dt_customer = Column(DateTime, doc="Date d'inscription du client")
    age = Column(Integer, doc="Âge du client (calculé)")
    customer_seniority = Column(Integer, doc="Ancienneté en mois")

    # ---- Composition du foyer ----
    kidhome = Column(Integer, doc="Nombre d'enfants (0-12 ans) au foyer")
    teenhome = Column(Integer, doc="Nombre d'adolescents (13-17 ans)")
    recency = Column(Integer, doc="Nombre de jours depuis la dernière interaction")

    # ---- Dépenses du client ----
    mnt_wines = Column(Float, doc="Montant dépensé en vins")
    mnt_fruits = Column(Float, doc="Montant dépensé en fruits")
    mnt_meat = Column(Float, doc="Montant dépensé en viandes")
    mnt_fish = Column(Float, doc="Montant dépensé en poissons")
    mnt_sweets = Column(Float, doc="Montant dépensé en bonbons/gâteaux")
    mnt_gold = Column(Float, doc="Montant dépensé en produits gold/luxe")

    # ---- Canaux utilisés par le client ----
    num_deals = Column(Integer, doc="Nombre de promotions utilisées")
    num_web = Column(Integer, doc="Achats effectués via le site web")
    num_catalog = Column(Integer, doc="Achats effectués via catalogue")
    num_store = Column(Integer, doc="Achats effectués en magasin")
    num_web_visits = Column(Integer, doc="Nombre de visites sur le site web")

    # ---- Résultats de clustering ----
    cluster_kmeans = Column(Integer, nullable=True, doc="Cluster attribué par K-Means")
    cluster_cah = Column(Integer, nullable=True, doc="Cluster attribué par CAH")

    # ---- Relation vers PCA ----
    pca_results = relationship("PCAResult", back_populates="customer")



# =====================================================================
#                         ClusterProfile Model
# =====================================================================
class ClusterProfile(Base):
    """
    Modèle représentant le profil d’un cluster.

    Chaque enregistrement contient :
    - Le type de modèle utilisé (KMeans, CAH)
    - Le numéro du cluster
    - Un dictionnaire JSON contenant des statistiques (moyennes, médianes, effectifs)
    """

    __tablename__ = "cluster_profiles"

    id = Column(Integer, primary_key=True, autoincrement=True)

    model_type = Column(String, doc="Type de modèle ('kmeans' ou 'cah')")
    cluster_label = Column(Integer, doc="Numéro du cluster")
    profile_data = Column(JSON, doc="Résumé statistique du cluster au format JSON")

    created_at = Column(DateTime, default=datetime.utcnow, doc="Horodatage de création")



# =====================================================================
#                          PCAResult Model
# =====================================================================
class PCAResult(Base):
    """
    Stocke les coordonnées PCA d’un client pour visualisation.

    Permet de tracer les clients dans l’espace PC1 / PC2 afin de visualiser
    la séparation entre clusters.
    """

    __tablename__ = "pca_results"

    id = Column(Integer, primary_key=True, autoincrement=True)

    # ---- Lien vers le client ----
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=True)

    # ---- Coordonnées PCA ----
    pc1 = Column(Float, doc="Valeur de la première composante principale")
    pc2 = Column(Float, doc="Valeur de la deuxième composante principale")

    # ---- Informations complémentaires ----
    model_type = Column(String, doc="Type de clustering associé (kmeans/cah)")
    created_at = Column(DateTime, default=datetime.utcnow, doc="Horodatage d'enregistrement")

    # ---- Relation inverse ----
    customer = relationship("Customer", back_populates="pca_results")
