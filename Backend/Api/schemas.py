# # ============================================================
# #   schemas.py
# #   Pydantic Schemas pour le projet Clustering (compatible V2)
# # ============================================================

# from pydantic import BaseModel, ConfigDict
# from datetime import datetime
# from typing import Optional, List, Dict, Any

# # ============================================================
# #   CUSTOMER SCHEMAS
# # ============================================================

# class CustomerBase(BaseModel):
#     """Schéma de base pour les clients"""
#     year_birth: Optional[int] = None
#     education: Optional[str] = None
#     marital_status: Optional[str] = None
#     income: Optional[float] = None
#     dt_customer: Optional[datetime] = None
#     age: Optional[int] = None
#     customer_seniority: Optional[int] = None

#     kidhome: Optional[int] = 0
#     teenhome: Optional[int] = 0

#     recency: Optional[int] = None
#     mnt_wines: Optional[float] = 0.0
#     mnt_fruits: Optional[float] = 0.0
#     mnt_meat: Optional[float] = 0.0
#     mnt_fish: Optional[float] = 0.0
#     mnt_sweets: Optional[float] = 0.0
#     mnt_gold: Optional[float] = 0.0

#     num_deals: Optional[int] = 0
#     num_web: Optional[int] = 0
#     num_catalog: Optional[int] = 0
#     num_store: Optional[int] = 0
#     num_web_visits: Optional[int] = 0


# class CustomerCreate(CustomerBase):
#     """Schéma pour l'insertion d'un client"""
#     pass


# class CustomerUpdate(BaseModel):
#     """Schéma pour la mise à jour des clusters"""
#     cluster_kmeans: Optional[int] = None
#     cluster_cah: Optional[int] = None


# class CustomerOut(CustomerBase):
#     """Schéma de sortie pour les endpoints"""
#     id: int
#     cluster_kmeans: Optional[int] = None
#     cluster_cah: Optional[int] = None
#     created_at: datetime

#     model_config = ConfigDict(from_attributes=True)


# # ============================================================
# #   CLUSTER PROFILE SCHEMAS
# # ============================================================

# class ClusterProfileBase(BaseModel):
#     """Schéma de base pour le profil d'un cluster"""
#     model_type: str
#     cluster_label: int
#     profile_data: Dict[str, Any]


# class ClusterProfileCreate(ClusterProfileBase):
#     """Schéma pour créer un profil de cluster"""
#     pass


# class ClusterProfileOut(ClusterProfileBase):
#     """Schéma de sortie pour les profils"""
#     id: int
#     created_at: datetime

#     model_config = ConfigDict(from_attributes=True)


# # ============================================================
# #   PCA RESULT SCHEMAS
# # ============================================================

# class PCAResultBase(BaseModel):
#     """Schéma de base pour les coordonnées PCA d'un client"""
#     customer_id: int
#     pc1: float
#     pc2: float
#     model_type: str


# class PCAResultCreate(PCAResultBase):
#     """Schéma pour créer une entrée PCA"""
#     pass


# class PCAResultOut(PCAResultBase):
#     """Schéma de sortie pour les résultats PCA"""
#     id: int
#     created_at: datetime

#     model_config = ConfigDict(from_attributes=True)


# # ============================================================
# #   API RESPONSE SCHEMAS
# # ============================================================

# class ClusterResultResponse(BaseModel):
#     """Réponse après calcul d'un clustering"""
#     message: str
#     model_type: str
#     n_clusters: int
#     silhouette_score: float
#     created_profiles: int


# class PCAResponse(BaseModel):
#     """Réponse après application de PCA"""
#     message: str
#     model_type: str
#     n_points: int


# class StandardResponse(BaseModel):
#     """Réponse standard pour endpoints génériques"""
#     status: str
#     data: Optional[Dict[str, Any]] = None
#     message: Optional[str] = None









######################################



# ============================================================
#   schemas.py
#   Pydantic Schemas pour le projet Clustering (compatible V2)
# ============================================================

from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from typing import Optional, List, Dict, Any

# ============================================================
#   CUSTOMER SCHEMAS
# ============================================================

class CustomerBase(BaseModel):
    """Schéma de base pour les attributs clients (utilisé pour le clustering)"""
    year_birth: Optional[int] = None
    education: Optional[str] = None
    marital_status: Optional[str] = None
    income: Optional[float] = 0.0
    dt_customer: Optional[datetime] = None
    age: Optional[int] = None
    customer_seniority: Optional[int] = None

    kidhome: Optional[int] = 0
    teenhome: Optional[int] = 0

    recency: Optional[int] = 0
    mnt_wines: Optional[float] = 0.0
    mnt_fruits: Optional[float] = 0.0
    mnt_meat: Optional[float] = 0.0
    mnt_fish: Optional[float] = 0.0
    mnt_sweets: Optional[float] = 0.0
    mnt_gold: Optional[float] = 0.0

    num_deals: Optional[int] = 0
    num_web: Optional[int] = 0
    num_catalog: Optional[int] = 0
    num_store: Optional[int] = 0
    num_web_visits: Optional[int] = 0


class ClientSchema(CustomerBase):
    """
    Schéma utilisé spécifiquement pour la réception par lot (Batch).
    L'inclusion de l'ID est CRITIQUE pour permettre la mise à jour 
    de la colonne cluster_kmeans en base de données.
    """
    id: Optional[int] = None
    
    # Permet d'utiliser les noms de colonnes SQL directement
    model_config = ConfigDict(from_attributes=True)


class CustomerCreate(CustomerBase):
    """Schéma pour l'insertion d'un nouveau client"""
    pass


class CustomerUpdate(BaseModel):
    """Schéma pour mettre à jour les clusters d'un client existant"""
    cluster_kmeans: Optional[int] = None
    cluster_cah: Optional[int] = None


class CustomerOut(CustomerBase):
    """Schéma de sortie enrichi pour les endpoints d'affichage"""
    id: int
    cluster_kmeans: Optional[int] = None
    cluster_cah: Optional[int] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


# ============================================================
#   CLUSTER PROFILE SCHEMAS (Marketing & Insights)
# ============================================================

class ClusterProfileBase(BaseModel):
    """Description métier d'un segment identifié"""
    model_type: str
    cluster_label: int
    profile_data: Dict[str, Any]


class ClusterProfileOut(ClusterProfileBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


# ============================================================
#   PCA RESULT SCHEMAS (Visualisation 2D)
# ============================================================

class PCAResultBase(BaseModel):
    customer_id: int
    pc1: float
    pc2: float
    model_type: str


class PCAResultOut(PCAResultBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


# ============================================================
#   API RESPONSE SCHEMAS (Validation des retours)
# ============================================================

class ClusterResultResponse(BaseModel):
    """Résumé après une session d'entraînement ou de prédiction massive"""
    status: str = "success"
    message: str
    total_clients: int
    updated_in_db: bool = False
    results: Optional[List[Dict[str, Any]]] = None


class StandardResponse(BaseModel):
    """Réponse générique pour la santé de l'API ou les stats"""
    status: str
    data: Optional[Any] = None
    message: Optional[str] = None