from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from database import get_db
from models import Income, Expense
from pydantic import BaseModel
from datetime import date
from typing import Optional, List

router = APIRouter(prefix="/incomes", tags=["incomes"])


class IncomeCreate(BaseModel):
    date: date
    category: str
    description: Optional[str] = None
    amount: float


class IncomeOut(IncomeCreate):
    id: int
    class Config:
        from_attributes = True


class BalanceSummary(BaseModel):
    total_income: float
    total_expense: float
    balance: float


@router.get("/", response_model=List[IncomeOut])
def get_incomes(year: Optional[int] = None, month: Optional[int] = None, db: Session = Depends(get_db)):
    q = db.query(Income)
    if year:
        q = q.filter(func.extract('year', Income.date) == year)
    if month:
        q = q.filter(func.extract('month', Income.date) == month)
    return q.order_by(Income.date.desc()).all()


@router.post("/", response_model=IncomeOut)
def create_income(data: IncomeCreate, db: Session = Depends(get_db)):
    income = Income(**data.model_dump())
    db.add(income)
    db.commit()
    db.refresh(income)
    return income


@router.delete("/{income_id}")
def delete_income(income_id: int, db: Session = Depends(get_db)):
    income = db.query(Income).filter(Income.id == income_id).first()
    if income:
        db.delete(income)
        db.commit()
    return {"ok": True}


@router.get("/balance", response_model=BalanceSummary)
def get_balance(db: Session = Depends(get_db)):
    total_income = db.query(func.sum(Income.amount)).scalar() or 0
    total_expense = db.query(func.sum(Expense.amount)).scalar() or 0
    return BalanceSummary(
        total_income=total_income,
        total_expense=total_expense,
        balance=total_income - total_expense,
    )
