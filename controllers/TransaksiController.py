from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from config.db import get_db
from models.transaksi import Transaksi
from schemas import TransaksiCreate, TransaksiResponse
from utils.auth import get_current_active_user, check_staff, check_admin
from models.user import User

router = APIRouter()

@router.post("/", response_model=TransaksiResponse)
def create_transaksi(
    transaksi: TransaksiCreate,
    db: Session = Depends(get_db),
    user: User = Depends(check_staff)
):
    db_transaksi = Transaksi(**transaksi.dict())
    db.add(db_transaksi)
    db.commit()
    db.refresh(db_transaksi)
    return db_transaksi

@router.get("/", response_model=List[TransaksiResponse])
def read_transaksi(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_active_user)
):
    return db.query(Transaksi).offset(skip).limit(limit).all()

@router.get("/{transaksi_id}", response_model=TransaksiResponse)
def read_transaksi_by_id(
    transaksi_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_active_user)
):
    db_transaksi = db.query(Transaksi).filter(Transaksi.id == transaksi_id).first()
    if db_transaksi is None:
        raise HTTPException(status_code=404, detail="Transaksi not found")
    return db_transaksi

@router.put("/{transaksi_id}", response_model=TransaksiResponse)
def update_transaksi(
    transaksi_id: int,
    transaksi: TransaksiCreate,
    db: Session = Depends(get_db),
    user: User = Depends(check_staff)
):
    db_transaksi = db.query(Transaksi).filter(Transaksi.id == transaksi_id).first()
    if db_transaksi is None:
        raise HTTPException(status_code=404, detail="Transaksi not found")
    
    for var, value in transaksi.dict().items():
        setattr(db_transaksi, var, value)
    
    db.commit()
    db.refresh(db_transaksi)
    return db_transaksi

@router.delete("/{transaksi_id}")
def delete_transaksi(
    transaksi_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(check_admin)
):
    db_transaksi = db.query(Transaksi).filter(Transaksi.id == transaksi_id).first()
    if db_transaksi is None:
        raise HTTPException(status_code=404, detail="Transaksi not found")
    
    db.delete(db_transaksi)
    db.commit()
    return {"message": "Transaksi deleted successfully"}
