"""
crud.py
-------

Fichier contenant les fonctions CRUD (Create, Read, Update, Delete) utilisées pour
interagir avec les modèles SQLAlchemy du projet de segmentation client.

Ce module assure :
- La création et mise à jour des clients (Customer)
- L'insertion des profils statistiques de clusters (ClusterProfile)
- La sauvegarde des coordonnées PCA (PCAResult)
- La récupération de données pour exploitation analytique
- La gestion sécurisée des transactions SQLAlchemy

Les fonctions sont conçues pour être utilisées dans une API FastAPI, Flask ou un script.
"""

from typing import Dict, Any, List, Optional, Union
from sqlalchemy.orm import Session
from sqlalchemy import select
from datetime import datetime
import pandas as pd

from models import Customer, ClusterProfile, PCAResult

# =====================================================================
#                        CRUD SUR LE MODÈLE CUSTOMER
# =====================================================================

def create_customer(db: Session, customer_data: Dict[str, Any]) -> Customer:
    """
    Crée un nouveau client dans la base de données.

    Args:
        db (Session): Session SQLAlchemy active.
        customer_data (dict): Données du client (clé = nom attribut modèle).

    Returns:
        Customer : Instance du client nouvellement créé.

    Notes :
        - Aucun commit n'est fait ici ; il est attendu que l'appelant valide la transaction.
    """
    customer = Customer(**customer_data)
    db.add(customer)
    db.flush()  # Assure la génération d'un ID

    return customer



def update_customer(db: Session, customer: Customer, updates: Dict[str, Any]) -> Customer:
    """
    Met à jour les données d'un client existant.

    Args:
        db (Session): Session SQLAlchemy.
        customer (Customer): Instance à mettre à jour.
        updates (dict): Clé/valeurs correspondant aux colonnes du modèle.

    Returns:
        Customer : Client mis à jour.

    Raises:
        AttributeError : Si une clé du dict ne correspond à aucune colonne du modèle.
    """
    for key, value in updates.items():
        if hasattr(customer, key):
            setattr(customer, key, value)

    db.flush()
    return customer



def get_customer_by_id(db: Session, customer_id: int) -> Optional[Customer]:
    """
    Récupère un client par son identifiant.

    Args:
        db (Session): Session SQLAlchemy.
        customer_id (int): Identifiant du client.

    Returns:
        Customer | None
    """
    return db.get(Customer, customer_id)



def get_customers_by_cluster(
    db: Session, cluster_type: str, cluster_label: int, limit: int = 200
) -> List[Customer]:
    """
    Récupère les clients appartenant à un cluster donné (kmeans ou CAH).

    Args:
        db (Session): Session active.
        cluster_type (str): 'cluster_kmeans' ou 'cluster_cah'.
        cluster_label (int): Numéro du cluster recherché.
        limit (int): Nombre max de clients retournés.

    Returns:
        List[Customer]
    """
    if cluster_type not in ("cluster_kmeans", "cluster_cah"):
        raise ValueError("cluster_type doit être 'cluster_kmeans' ou 'cluster_cah'")

    stmt = (
        select(Customer)
        .where(getattr(Customer, cluster_type) == cluster_label)
        .limit(limit)
    )
    return db.execute(stmt).scalars().all()

def bulk_upsert_customers(
    db: Session, df: pd.DataFrame, id_col: Optional[str] = None
) -> int:
    """
    Insère ou met à jour en masse des clients à partir d'un DataFrame.

    Args:
        db (Session): Session active.
        df (pd.DataFrame): Données clients (colonnes = attributs Customer).
        id_col (str, optional): Colonne identifiant unique (permet upsert). Si None → insert only.

    Returns:
        int : Nombre d'enregistrements insérés ou mis à jour.
    """
    if df.empty:
        return 0

    count = 0

    try:
        for _, row in df.iterrows():
            data = row.to_dict()

            if id_col and id_col in data and pd.notna(data[id_col]):
                existing = db.get(Customer, int(data[id_col]))
                if existing:
                    updates = {k: v for k, v in data.items() if hasattr(existing, k)}
                    update_customer(db, existing, updates)
                else:
                    create_customer(db, {k: v for k, v in data.items() if hasattr(Customer, k)})
            else:
                create_customer(db, {k: v for k, v in data.items() if hasattr(Customer, k)})

            count += 1

        db.commit()
        return count

    except Exception as e:
        db.rollback()
        raise
# =====================================================================
#                GESTION DES PROFILS STATISTIQUES DE CLUSTERS
# =====================================================================

def save_cluster_profiles(
    db: Session, model_type: str, profiles: Dict[Union[int, str], Dict[str, Any]]
) -> int:
    """
    Sauvegarde les profils statistiques des clusters.

    Args:
        db (Session)
        model_type (str): "kmeans" ou "cah".
        profiles (dict): {label_cluster: {stat: valeur, ...}}

    Returns:
        int : Nombre de profils insérés.
    """
    inserted = 0

    try:
        for label, pdata in profiles.items():
            profile = ClusterProfile(
                model_type=model_type,
                cluster_label=int(label),
                profile_data=pdata,
                created_at=datetime.utcnow()
            )
            db.add(profile)
            inserted += 1

        db.commit()
        return inserted

    except Exception:
        db.rollback()
        raise
# =====================================================================
#                   GESTION DES COORDONNÉES PCA
# =====================================================================

def save_pca_results(
    db: Session,
    pca_df: pd.DataFrame,
    model_type: str,
    customer_id_col: Optional[str] = None
) -> int:
    """
    Sauvegarde les coordonnées PCA dans la base.

    Args:
        db (Session)
        pca_df (DataFrame): Colonnes nécessaires : PC1, PC2 (+ cluster optionnel)
        model_type (str): 'kmeans' ou 'cah'
        customer_id_col (str, optional): Si fourni, indiquera quel client correspond aux coordonnées PCA.

    Returns:
        int : Nombre d'enregistrements créés.
    """
    if pca_df.empty:
        return 0

    inserted = 0

    try:
        for _, row in pca_df.iterrows():
            customer_id = row[customer_id_col] if customer_id_col and customer_id_col in pca_df.columns else None

            pca = PCAResult(
                customer_id=int(customer_id) if customer_id not in (None, pd.NA) else None,
                pc1=float(row["PC1"]),
                pc2=float(row["PC2"]),
                model_type=model_type,
                created_at=datetime.utcnow()
            )
            db.add(pca)
            inserted += 1

        db.commit()
        return inserted

    except Exception:
        db.rollback()
        raise
# =====================================================================
#                     FONCTIONS DE RÉCUPÉRATION D'ANALYSES
# =====================================================================

def get_latest_cluster_profiles(
    db: Session, model_type: Optional[str] = None, limit: int = 100
) -> List[ClusterProfile]:
    """
    Récupère les profils de clusters les plus récents.

    Args:
        db (Session)
        model_type (str, optional): Filtre 'kmeans' ou 'cah'
        limit (int)

    Returns:
        List[ClusterProfile]
    """
    q = select(ClusterProfile).order_by(ClusterProfile.created_at.desc()).limit(limit)

    if model_type:
        q = (
            select(ClusterProfile)
            .where(ClusterProfile.model_type == model_type)
            .order_by(ClusterProfile.created_at.desc())
            .limit(limit)
        )

    return db.execute(q).scalars().all()

def get_pca_coords(
    db: Session, model_type: Optional[str] = None, limit: int = 1000
) -> List[PCAResult]:
    """
    Récupère les coordonnées PCA stockées.

    Args:
        db (Session)
        model_type (str, optional): "kmeans" ou "cah"
        limit (int)

    Returns:
        List[PCAResult]
    """
    q = select(PCAResult).order_by(PCAResult.created_at.desc()).limit(limit)

    if model_type:
        q = (
            select(PCAResult)
            .where(PCAResult.model_type == model_type)
            .order_by(PCAResult.created_at.desc())
            .limit(limit)
        )

    return db.execute(q).scalars().all()


################################################################"





"""
crud.py
-------

Module contenant les fonctions CRUD (Create, Read, Update, Delete) utilisées pour
interagir avec les modèles SQLAlchemy du projet de segmentation client.

Ce module remplit plusieurs rôles essentiels :

1. Gérer l’insertion et la mise à jour des clients (Customer)
2. Enregistrer les profils statistiques issus du clustering (ClusterProfile)
3. Sauvegarder les coordonnées PCA pour les visualisations (PCAResult)
4. Fournir des fonctions de lecture optimisées pour l’analyse
5. Garantir une gestion propre des transactions avec SQLAlchemy

Ce module sert de couche d’abstraction entre :
- l’API (FastAPI/Flask)
- les scripts ML
- la base de données PostgreSQL

Il permet d’éviter de manipuler SQL directement dans les routes ou notebooks.
"""

from typing import Dict, Any, List, Optional, Union
from sqlalchemy.orm import Session
from sqlalchemy import select
from datetime import datetime
import pandas as pd

from models import Customer, ClusterProfile, PCAResult


# =====================================================================
#                 CRUD SUR LE MODÈLE CUSTOMER (CLIENTS)
# =====================================================================

def create_customer(db: Session, customer_data: Dict[str, Any]) -> Customer:
    """
    Crée un client dans la base de données.

    Args:
        db (Session): Session SQLAlchemy active.
        customer_data (dict): Données du client (clé = attribut Customer).

    Returns:
        Customer : Instance du client nouvellement créé.

    Notes :
        - db.add() ajoute l’objet dans la transaction en cours
        - db.flush() force la base à générer l’ID sans commit
        - Le commit doit être fait par l'appelant pour garder le contrôle
    """
    customer = Customer(**customer_data)
    db.add(customer)
    db.flush()
    return customer



def update_customer(db: Session, customer: Customer, updates: Dict[str, Any]) -> Customer:
    """
    Met à jour un client existant dans la base.

    Args:
        db (Session)
        customer (Customer): Instance à mettre à jour.
        updates (dict): Valeurs mises à jour.

    Raises:
        AttributeError : Si une clé du dict ne correspond à aucun attribut du modèle.

    Return:
        Customer : Instance mise à jour.
    """
    for key, value in updates.items():
        if hasattr(customer, key):
            setattr(customer, key, value)

    db.flush()
    return customer



def get_customer_by_id(db: Session, customer_id: int) -> Optional[Customer]:
    """
    Récupère un client via son ID.

    Args:
        db (Session)
        customer_id (int)

    Returns:
        Customer | None
    """
    return db.get(Customer, customer_id)



def get_customers_by_cluster(
    db: Session, cluster_type: str, cluster_label: int, limit: int = 200
) -> List[Customer]:
    """
    Récupère les clients d'un cluster spécifique.

    Args:
        db (Session)
        cluster_type (str): 'cluster_kmeans' ou 'cluster_cah'
        cluster_label (int)
        limit (int)

    Returns:
        List[Customer]

    Raises:
        ValueError : Si cluster_type est invalide.
    """
    if cluster_type not in ("cluster_kmeans", "cluster_cah"):
        raise ValueError("cluster_type doit être 'cluster_kmeans' ou 'cluster_cah'")

    stmt = (
        select(Customer)
        .where(getattr(Customer, cluster_type) == cluster_label)
        .limit(limit)
    )
    return db.execute(stmt).scalars().all()



def bulk_upsert_customers(
    db: Session, df: pd.DataFrame, id_col: Optional[str] = None
) -> int:
    """
    Insère ou met à jour massivement des clients à partir d’un DataFrame.

    Args:
        db (Session)
        df (DataFrame) : Chaque ligne = un client
        id_col (str, optional): Colonne identifiant unique pour upsert.
                               Si None → insert uniquement.

    Returns:
        int : Nombre de lignes traitées (insert + update)

    Fonctionnement :
        - Parcours toutes les lignes du DataFrame
        - Si id_col est fourni → update ou insert
        - Sinon → insert systématique
    """
    if df.empty:
        return 0

    count = 0

    try:
        for _, row in df.iterrows():
            data = row.to_dict()

            # — UP SERT (mettre à jour si existe, sinon insérer)
            if id_col and id_col in data and pd.notna(data[id_col]):
                existing = db.get(Customer, int(data[id_col]))

                if existing:
                    updates = {k: v for k, v in data.items() if hasattr(existing, k)}
                    update_customer(db, existing, updates)

                else:
                    create_customer(db, {k: v for k, v in data.items() if hasattr(Customer, k)})

            # — INSERT SIMPLE
            else:
                create_customer(db, {k: v for k, v in data.items() if hasattr(Customer, k)})

            count += 1

        db.commit()
        return count

    except Exception:
        db.rollback()
        raise


# =====================================================================
#       GESTION DES PROFILS DE CLUSTERS (K-MEANS / CAH)
# =====================================================================

def save_cluster_profiles(
    db: Session, model_type: str, profiles: Dict[Union[int, str], Dict[str, Any]]
) -> int:
    """
    Sauvegarde les profils statistiques de clusters.

    Args:
        db (Session)
        model_type (str): 'kmeans' ou 'cah'
        profiles (dict): {label_cluster: stats_json}

    Returns:
        int : Nombre de profils insérés.

    Notes :
        - profile_data contient des statistiques (moyennes, médianes...)
        - Chaque insertion est timestampée (created_at)
    """
    inserted = 0

    try:
        for label, pdata in profiles.items():
            profile = ClusterProfile(
                model_type=model_type,
                cluster_label=int(label),
                profile_data=pdata,
                created_at=datetime.utcnow()
            )
            db.add(profile)
            inserted += 1

        db.commit()
        return inserted

    except Exception:
        db.rollback()
        raise


# =====================================================================
#                    GESTION DES COORDONNÉES PCA
# =====================================================================

def save_pca_results(
    db: Session,
    pca_df: pd.DataFrame,
    model_type: str,
    customer_id_col: Optional[str] = None
) -> int:
    """
    Enregistre les coordonnées PCA dans la base.

    Args:
        db (Session)
        pca_df (DataFrame): Doit contenir 'PC1' et 'PC2'
        model_type (str): kmeans ou cah
        customer_id_col (str, optional): Colonne mappant chaque point à un client

    Returns:
        int : Nombre d'enregistrements créés.

    Utilité :
        - Permet de tracer PC1/PC2 sur l’interface
        - Permet d’associer un point PCA à un client précis
    """
    if pca_df.empty:
        return 0

    inserted = 0

    try:
        for _, row in pca_df.iterrows():
            customer_id = row[customer_id_col] if customer_id_col and customer_id_col in pca_df.columns else None

            pca = PCAResult(
                customer_id=int(customer_id) if customer_id not in (None, pd.NA) else None,
                pc1=float(row["PC1"]),
                pc2=float(row["PC2"]),
                model_type=model_type,
                created_at=datetime.utcnow()
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
    """
    Récupère les profils de clusters (les plus récents d'abord).

    Args:
        db (Session)
        model_type (str, optional): 'kmeans' ou 'cah'
        limit (int)

    Returns:
        List[ClusterProfile]
    """
    q = select(ClusterProfile).order_by(ClusterProfile.created_at.desc()).limit(limit)

    if model_type:
        q = (
            select(ClusterProfile)
            .where(ClusterProfile.model_type == model_type)
            .order_by(ClusterProfile.created_at.desc())
            .limit(limit)
        )

    return db.execute(q).scalars().all()



def get_pca_coords(
    db: Session, model_type: Optional[str] = None, limit: int = 1000
) -> List[PCAResult]:
    """
    Récupère les coordonnées PCA stockées dans la base.

    Args:
        db (Session)
        model_type (str, optional): 'kmeans' ou 'cah'
        limit (int)

    Returns:
        List[PCAResult]
    """
    q = select(PCAResult).order_by(PCAResult.created_at.desc()).limit(limit)

    if model_type:
        q = (
            select(PCAResult)
            .where(PCAResult.model_type == model_type)
            .order_by(PCAResult.created_at.desc())
            .limit(limit)
        )

    return db.execute(q).scalars().all()
