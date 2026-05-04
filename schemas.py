from pydantic import BaseModel
from datetime import date
from typing import Optional, List


class BudgetCreate(BaseModel):
    year: int
    month: int
    category: str
    amount: float


class BudgetUpdate(BaseModel):
    amount: float


class BudgetOut(BudgetCreate):
    id: int
    class Config:
        from_attributes = True


class ExpenseCreate(BaseModel):
    date: date
    category: str
    description: Optional[str] = None
    amount: float


class ExpenseOut(ExpenseCreate):
    id: int
    class Config:
        from_attributes = True


class IncomeCreate(BaseModel):
    date: date
    category: str
    description: Optional[str] = None
    amount: float


class IncomeOut(IncomeCreate):
    id: int
    class Config:
        from_attributes = True


class BalanceOut(BaseModel):
    total_income: float
    total_expense: float
    balance: float


class BudgetSummary(BaseModel):
    category: str
    budget: float
    spent: float
    remaining: float


class SavingsGoalCreate(BaseModel):
    name: str
    emoji: Optional[str] = "🎯"
    target_amount: float
    current_amount: Optional[float] = 0.0
    deadline: Optional[str] = None


class SavingsGoalUpdate(BaseModel):
    name: Optional[str] = None
    emoji: Optional[str] = None
    target_amount: Optional[float] = None
    current_amount: Optional[float] = None
    deadline: Optional[str] = None


class SavingsGoalOut(BaseModel):
    id: int
    name: str
    emoji: str
    target_amount: float
    current_amount: float
    deadline: Optional[str]
    class Config:
        from_attributes = True


class HabitCreate(BaseModel):
    name: str
    emoji: Optional[str] = "⭐"


class HabitLogCreate(BaseModel):
    date: date


class HabitOut(BaseModel):
    id: int
    name: str
    emoji: str
    streak: int = 0
    logs: List[str] = []
    class Config:
        from_attributes = True


class DebtCreate(BaseModel):
    name: str
    creditor: str
    debt_type: Optional[str] = "อื่นๆ"
    total_amount: float
    remaining: float
    monthly_payment: Optional[float] = 0.0
    interest_rate: Optional[float] = 0.0
    due_date: Optional[str] = None
    note: Optional[str] = None


class DebtUpdate(BaseModel):
    name: Optional[str] = None
    creditor: Optional[str] = None
    debt_type: Optional[str] = None
    total_amount: Optional[float] = None
    remaining: Optional[float] = None
    monthly_payment: Optional[float] = None
    interest_rate: Optional[float] = None
    due_date: Optional[str] = None
    note: Optional[str] = None


class DebtOut(BaseModel):
    id: int
    name: str
    creditor: str
    debt_type: str
    total_amount: float
    remaining: float
    monthly_payment: float
    interest_rate: float
    due_date: Optional[str]
    note: Optional[str]
    class Config:
        from_attributes = True
