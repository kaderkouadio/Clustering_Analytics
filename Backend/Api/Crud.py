"""
crud.py
-------
Couche d'accès aux données (DAL) pour le projet Clustering Analytics.
Assure l'interface entre SQLAlchemy et la logique métier.
"""

import logging
import pandas as pd
from sqlalchemy.orm import Session
from sqlalchemy import select
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional, Union, Tuple

# Import des modèles depuis votre structure Backend.Api
# from models import ClientData, ClusterProfile, PCAResult
try:
    from models import ClientData, ClusterProfile, PCAResult
except ImportError:
    from .models import ClientData, ClusterProfile, PCAResult # Le point signifie "dans le même dossier"



# Configuration du logger
logger = logging.getLogger(__name__)

# =====================================================================
#                 CRUD SUR LE MODÈLE CLIENTDATA
# =====================================================================

def create_client(db: Session, client_data: Dict[str, Any]) -> ClientData:
    """Crée un client. Flush pour générer l'ID sans commit immédiat."""
    client = ClientData(**client_data)
    db.add(client)
    db.flush() 
    return client

def update_client(db: Session, client: ClientData, updates: Dict[str, Any]) -> ClientData:
    """Met à jour les attributs d'un client existant."""
    for key, value in updates.items():
        if hasattr(client, key):
            setattr(client, key, value)
    db.flush()
    return client

def get_client_by_id(db: Session, client_id: int) -> Optional[ClientData]:
    """Récupération par clé primaire."""
    return db.get(ClientData, client_id)

def get_clients_by_cluster(
    db: Session, cluster_type: str, cluster_label: int, limit: int = 200
) -> List[ClientData]:
    """Filtre les clients par segment (kmeans ou cah)."""
    if cluster_type not in ("cluster_kmeans", "cluster_cah"):
        raise ValueError("cluster_type doit être 'cluster_kmeans' ou 'cluster_cah'")

    stmt = (
        select(ClientData)
        .where(getattr(ClientData, cluster_type) == cluster_label)
        .limit(limit)
    )
    return db.execute(stmt).scalars().all()

# def bulk_upsert_clients(db: Session, df: pd.DataFrame, id_col: Optional[str] = None) -> int:
#     """
#     Insère ou met à jour massivement des clients.
#     Gère le rollback automatique en cas d'échec.
#     """
#     if df.empty:
#         return 0
#     count = 0
#     try:
#         for _, row in df.iterrows():
#             data = row.to_dict()
#             # Logique Upsert
#             if id_col and id_col in data and pd.notna(data[id_col]):
#                 existing = db.get(ClientData, int(data[id_col]))
#                 if existing:
#                     # On ne met à jour que les colonnes présentes dans le modèle
#                     updates = {k: v for k, v in data.items() if hasattr(existing, k)}
#                     update_client(db, existing, updates)
#                 else:
#                     create_client(db, {k: v for k, v in data.items() if hasattr(ClientData, k)})
#             else:
#                 create_client(db, {k: v for k, v in data.items() if hasattr(ClientData, k)})
#             count += 1

#         db.commit()
#         return count
#     except Exception:
#         db.rollback()
#         raise



def bulk_upsert_clients(db: Session, df: pd.DataFrame, id_col: Optional[str] = None) -> Tuple[int, int]:
    """
    Insère ou ignore les doublons.
    Retourne (nombre_insérés, nombre_doublons_ignorés).
    """
    if df.empty:
        return 0, 0
    
    new_count = 0
    skip_count = 0
    
    try:
        for _, row in df.iterrows():
            data = row.to_dict()
            existing = None

            # 1. Recherche par ID (si présent)
            if id_col and id_col in data and pd.notna(data[id_col]):
                existing = db.get(ClientData, int(data[id_col]))
            
            # 2. Recherche par critères métier (si pas d'ID ou ID non trouvé)
            # Empêche d'insérer 2 fois le même client du CSV lors de plusieurs runs
            if not existing:
                existing = db.query(ClientData).filter(
                    ClientData.income == data.get('income'),
                    ClientData.year_birth == data.get('year_birth'),
                    ClientData.dt_customer == data.get('dt_customer')
                ).first()

            if existing:
                # Optionnel : Vous pourriez mettre à jour ici. 
                # Pour l'ingestion initiale, on choisit souvent d'ignorer (skip)
                skip_count += 1
                continue 
            
            # 3. Création du nouveau client
            # On ne garde que les clés qui existent vraiment dans le modèle SQLAlchemy
            clean_data = {k: v for k, v in data.items() if hasattr(ClientData, k)}
            new_client = ClientData(**clean_data)
            db.add(new_client)
            new_count += 1

        db.commit()
        return new_count, skip_count

    except Exception as e:
        db.rollback()
        logger.error(f"Erreur lors du bulk_upsert : {e}")
        raise

# =====================================================================
#             GESTION DES PROFILS DE CLUSTERS
# =====================================================================

def save_cluster_profiles(
    db: Session, model_type: str, profiles: Dict[Union[int, str], Dict[str, Any]]
) -> int:
    """Enregistre les KPIs agrégés par cluster."""
    inserted = 0
    try:
        for label, pdata in profiles.items():
            profile = ClusterProfile(
                model_type=model_type,
                cluster_label=int(label),
                profile_data=pdata,
                created_at=datetime.now(timezone.utc) # Format aware recommandé
            )
            db.add(profile)
            inserted += 1
        db.commit()
        return inserted
    except Exception:
        db.rollback()
        raise

# =====================================================================
#                  GESTION DES COORDONNÉES PCA
# =====================================================================

def save_pca_results(
    db: Session, pca_df: pd.DataFrame, model_type: str, client_id_col: Optional[str] = None
) -> int:
    """Enregistre les projections PCA pour visualisation 2D."""
    if pca_df.empty:
        return 0
    inserted = 0
    try:
        for _, row in pca_df.iterrows():
            c_id = row[client_id_col] if client_id_col and client_id_col in pca_df.columns else None
            pca = PCAResult(
                client_id=int(c_id) if c_id not in (None, pd.NA) else None,
                pc1=float(row["PC1"]),
                pc2=float(row["PC2"]),
                model_type=model_type,
                created_at=datetime.now(timezone.utc)
            )
            db.add(pca)
            inserted += 1
        db.commit()
        return inserted
    except Exception:
        db.rollback()
        raise

# =====================================================================
#                     FONCTIONS DE RÉCUPÉRATION
# =====================================================================

def get_latest_cluster_profiles(
    db: Session, model_type: Optional[str] = None, limit: int = 100
) -> List[ClusterProfile]:
    """Récupère les derniers profils générés."""
    stmt = select(ClusterProfile).order_by(ClusterProfile.created_at.desc())
    if model_type:
        stmt = stmt.where(ClusterProfile.model_type == model_type)
    return db.execute(stmt.limit(limit)).scalars().all()

def get_pca_coords(
    db: Session, model_type: Optional[str] = None, limit: int = 1000
) -> List[PCAResult]:
    """Récupère les points pour le scatter plot."""
    stmt = select(PCAResult).order_by(PCAResult.created_at.desc())
    if model_type:
        stmt = stmt.where(PCAResult.model_type == model_type)
    return db.execute(stmt.limit(limit)).scalars().all()