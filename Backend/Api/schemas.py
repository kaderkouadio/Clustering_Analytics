# ============================================================
#   schemas.py
#   Pydantic Schemas pour le projet Clustering (compatible V2)
# ============================================================

from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional, List, Dict, Any

# ============================================================
#   CUSTOMER SCHEMAS
# ============================================================

class CustomerBase(BaseModel):
    """Schéma de base pour les clients"""
    year_birth: Optional[int] = None
    education: Optional[str] = None
    marital_status: Optional[str] = None
    income: Optional[float] = None
    dt_customer: Optional[datetime] = None
    age: Optional[int] = None
    customer_seniority: Optional[int] = None

    kidhome: Optional[int] = 0
    teenhome: Optional[int] = 0

    recency: Optional[int] = None
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


class CustomerCreate(CustomerBase):
    """Schéma pour l'insertion d'un client"""
    pass


class CustomerUpdate(BaseModel):
    """Schéma pour la mise à jour des clusters"""
    cluster_kmeans: Optional[int] = None
    cluster_cah: Optional[int] = None


class CustomerOut(CustomerBase):
    """Schéma de sortie pour les endpoints"""
    id: int
    cluster_kmeans: Optional[int] = None
    cluster_cah: Optional[int] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


# ============================================================
#   CLUSTER PROFILE SCHEMAS
# ============================================================

class ClusterProfileBase(BaseModel):
    """Schéma de base pour le profil d'un cluster"""
    model_type: str
    cluster_label: int
    profile_data: Dict[str, Any]


class ClusterProfileCreate(ClusterProfileBase):
    """Schéma pour créer un profil de cluster"""
    pass


class ClusterProfileOut(ClusterProfileBase):
    """Schéma de sortie pour les profils"""
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


# ============================================================
#   PCA RESULT SCHEMAS
# ============================================================

class PCAResultBase(BaseModel):
    """Schéma de base pour les coordonnées PCA d'un client"""
    customer_id: int
    pc1: float
    pc2: float
    model_type: str


class PCAResultCreate(PCAResultBase):
    """Schéma pour créer une entrée PCA"""
    pass


class PCAResultOut(PCAResultBase):
    """Schéma de sortie pour les résultats PCA"""
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


# ============================================================
#   API RESPONSE SCHEMAS
# ============================================================

class ClusterResultResponse(BaseModel):
    """Réponse après calcul d'un clustering"""
    message: str
    model_type: str
    n_clusters: int
    silhouette_score: float
    created_profiles: int


class PCAResponse(BaseModel):
    """Réponse après application de PCA"""
    message: str
    model_type: str
    n_points: int


class StandardResponse(BaseModel):
    """Réponse standard pour endpoints génériques"""
    status: str
    data: Optional[Dict[str, Any]] = None
    message: Optional[str] = None
