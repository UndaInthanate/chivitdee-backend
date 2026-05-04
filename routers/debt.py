from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Debt
from schemas import DebtCreate, DebtUpdate, DebtOut
from typing import List

router = APIRouter(prefix="/debts", tags=["debts"])


@router.get("/", response_model=List[DebtOut])
def get_debts(db: Session = Depends(get_db)):
    return db.query(Debt).order_by(Debt.id).all()


@router.post("/", response_model=DebtOut)
def create_debt(data: DebtCreate, db: Session = Depends(get_db)):
    debt = Debt(**data.model_dump())
    db.add(debt)
    db.commit()
    db.refresh(debt)
    return debt


@router.put("/{debt_id}", response_model=DebtOut)
def update_debt(debt_id: int, data: DebtUpdate, db: Session = Depends(get_db)):
    debt = db.query(Debt).filter(Debt.id == debt_id).first()
    if not debt:
        raise HTTPException(status_code=404, detail="ไม่พบรายการหนี้")
    for k, v in data.model_dump(exclude_none=True).items():
        setattr(debt, k, v)
    db.commit()
    db.refresh(debt)
    return debt


@router.delete("/{debt_id}")
def delete_debt(debt_id: int, db: Session = Depends(get_db)):
    debt = db.query(Debt).filter(Debt.id == debt_id).first()
    if not debt:
        raise HTTPException(status_code=404, detail="ไม่พบรายการหนี้")
    db.delete(debt)
    db.commit()
    return {"ok": True}
