from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import extract, func
from database import get_db
from models import Income, Expense
from schemas import IncomeCreate, IncomeOut, BalanceOut
from typing import List

router = APIRouter(prefix="/incomes", tags=["incomes"])


@router.get("/", response_model=List[IncomeOut])
def get_incomes(year: int, month: int, db: Session = Depends(get_db)):
    return db.query(Income).filter(
        extract("year", Income.date) == year,
        extract("month", Income.date) == month,
    ).order_by(Income.date.desc()).all()


@router.post("/", response_model=IncomeOut)
def create_income(data: IncomeCreate, db: Session = Depends(get_db)):
    inc = Income(**data.model_dump())
    db.add(inc)
    db.commit()
    db.refresh(inc)
    return inc


@router.delete("/{income_id}")
def delete_income(income_id: int, db: Session = Depends(get_db)):
    inc = db.query(Income).filter(Income.id == income_id).first()
    if inc:
        db.delete(inc)
        db.commit()
    return {"ok": True}


@router.get("/balance", response_model=BalanceOut)
def get_balance(db: Session = Depends(get_db)):
    total_income = db.query(func.sum(Income.amount)).scalar() or 0.0
    total_expense = db.query(func.sum(Expense.amount)).scalar() or 0.0
    return BalanceOut(
        total_income=total_income,
        total_expense=total_expense,
        balance=total_income - total_expense,
    )
