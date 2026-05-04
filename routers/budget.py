from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
import models, schemas
from database import get_db

router = APIRouter(prefix="/budgets", tags=["budgets"])


@router.post("/", response_model=schemas.BudgetOut, status_code=201)
def create_budget(payload: schemas.BudgetCreate, db: Session = Depends(get_db)):
    existing = db.query(models.MonthlyBudget).filter_by(
        year=payload.year, month=payload.month, category=payload.category
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Budget for this category/month already exists")
    budget = models.MonthlyBudget(**payload.model_dump())
    db.add(budget)
    db.commit()
    db.refresh(budget)
    return budget


@router.get("/", response_model=List[schemas.BudgetOut])
def list_budgets(year: int, month: int, db: Session = Depends(get_db)):
    return db.query(models.MonthlyBudget).filter_by(year=year, month=month).all()


@router.put("/{budget_id}", response_model=schemas.BudgetOut)
def update_budget(budget_id: int, payload: schemas.BudgetUpdate, db: Session = Depends(get_db)):
    budget = db.get(models.MonthlyBudget, budget_id)
    if not budget:
        raise HTTPException(status_code=404, detail="Budget not found")
    budget.amount = payload.amount
    db.commit()
    db.refresh(budget)
    return budget


@router.delete("/{budget_id}", status_code=204)
def delete_budget(budget_id: int, db: Session = Depends(get_db)):
    budget = db.get(models.MonthlyBudget, budget_id)
    if not budget:
        raise HTTPException(status_code=404, detail="Budget not found")
    db.delete(budget)
    db.commit()


@router.get("/summary", response_model=List[schemas.BudgetSummary])
def budget_summary(year: int, month: int, db: Session = Depends(get_db)):
    budgets = db.query(models.MonthlyBudget).filter_by(year=year, month=month).all()

    spent_rows = (
        db.query(models.Expense.category, func.sum(models.Expense.amount))
        .filter(
            func.extract("year", models.Expense.date) == year,
            func.extract("month", models.Expense.date) == month,
        )
        .group_by(models.Expense.category)
        .all()
    )
    spent_map = {row[0]: row[1] for row in spent_rows}

    return [
        schemas.BudgetSummary(
            category=b.category,
            budget=b.amount,
            spent=spent_map.get(b.category, 0.0),
            remaining=b.amount - spent_map.get(b.category, 0.0),
        )
        for b in budgets
    ]
