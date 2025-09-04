from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime
from ..db import get_db
from .. import models, schemas

router = APIRouter(prefix="/transactions", tags=["transactions"])


# ➡️ Liste des transactions (pagination, filtres, ou all=true)
@router.get("", response_model=schemas.Page)
def list_transactions(
    db: Session = Depends(get_db),
    all: bool = Query(False, description="Si true, renvoie toutes les transactions sans pagination"),
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=200),
    merchant: Optional[str] = None,
    category: Optional[str] = None,
    date_from: Optional[datetime] = None,
    date_to: Optional[datetime] = None,
    min_amount: Optional[float] = None,
    max_amount: Optional[float] = None,
):
    q = db.query(models.Transaction)

    # ➡️ Filtres dynamiques
    if merchant:
        q = q.filter(models.Transaction.merchant.ilike(f"%{merchant}%"))
    if category:
        q = q.filter(models.Transaction.category == category)
    if date_from:
        q = q.filter(models.Transaction.timestamp >= date_from)
    if date_to:
        q = q.filter(models.Transaction.timestamp < date_to)
    if min_amount is not None:
        q = q.filter(models.Transaction.amount >= min_amount)
    if max_amount is not None:
        q = q.filter(models.Transaction.amount <= max_amount)

    # ➡️ Mode all=true
    if all:
        items = q.order_by(models.Transaction.timestamp.desc()).all()
        total = len(items)
        return {"items": items, "total": total, "page": 1, "size": total}

    # ➡️ Mode pagination
    total = q.count()
    items = (
        q.order_by(models.Transaction.timestamp.desc())
        .offset((page - 1) * size)
        .limit(size)
        .all()
    )
    return {"items": items, "total": total, "page": page, "size": size}


# ➡️ Créer une transaction
@router.post("", response_model=schemas.TransactionRead, status_code=201)
def create_transaction(payload: schemas.TransactionCreate, db: Session = Depends(get_db)):
    obj = models.Transaction(**payload.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


# ➡️ Récupérer une transaction par ID
@router.get("/{tx_id}", response_model=schemas.TransactionRead)
def get_transaction(tx_id: int, db: Session = Depends(get_db)):
    obj = db.get(models.Transaction, tx_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return obj


# ➡️ Supprimer une transaction
@router.delete("/{tx_id}", status_code=204)
def delete_transaction(tx_id: int, db: Session = Depends(get_db)):
    obj = db.get(models.Transaction, tx_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Transaction not found")
    db.delete(obj)
    db.commit()
# ➡️ Debug : compter les transactions
@router.get("/debug/count")
def debug_count(db: Session = Depends(get_db)):
    total = db.query(models.Transaction).count()
    return {"total_transactions": total}
