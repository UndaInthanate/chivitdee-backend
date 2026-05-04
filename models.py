from sqlalchemy import Column, Integer, String, Float, Date, UniqueConstraint, ForeignKey
from database import Base


class MonthlyBudget(Base):
    __tablename__ = "monthly_budgets"
    __table_args__ = (UniqueConstraint("year", "month", "category", name="uq_budget_year_month_category"),)

    id       = Column(Integer, primary_key=True, index=True)
    year     = Column(Integer, nullable=False)
    month    = Column(Integer, nullable=False)
    category = Column(String, nullable=False)
    amount   = Column(Float, nullable=False)


class Expense(Base):
    __tablename__ = "expenses"

    id          = Column(Integer, primary_key=True, index=True)
    date        = Column(Date, nullable=False)
    category    = Column(String, nullable=False)
    description = Column(String, nullable=True)
    amount      = Column(Float, nullable=False)


class SavingsGoal(Base):
    __tablename__ = "savings_goals"

    id             = Column(Integer, primary_key=True, index=True)
    name           = Column(String, nullable=False)
    emoji          = Column(String, default="🎯")
    target_amount  = Column(Float, nullable=False)
    current_amount = Column(Float, default=0.0)
    deadline       = Column(String, nullable=True)


class Habit(Base):
    __tablename__ = "habits"

    id    = Column(Integer, primary_key=True, index=True)
    name  = Column(String, nullable=False)
    emoji = Column(String, default="⭐")


class HabitLog(Base):
    __tablename__ = "habit_logs"
    __table_args__ = (UniqueConstraint("habit_id", "date", name="uq_habit_log"),)

    id       = Column(Integer, primary_key=True, index=True)
    habit_id = Column(Integer, ForeignKey("habits.id", ondelete="CASCADE"), nullable=False)
    date     = Column(Date, nullable=False)


class Debt(Base):
    __tablename__ = "debts"

    id             = Column(Integer, primary_key=True, index=True)
    name           = Column(String, nullable=False)       # ชื่อหนี้
    creditor       = Column(String, nullable=False)       # เจ้าหนี้
    debt_type      = Column(String, default="อื่นๆ")     # บ้าน/รถ/บัตรเครดิต/สินเชื่อ/อื่นๆ
    total_amount   = Column(Float, nullable=False)        # ยอดหนี้ทั้งหมด
    remaining      = Column(Float, nullable=False)        # ยอดคงเหลือ
    monthly_payment= Column(Float, default=0.0)           # ผ่อนต่อเดือน
    interest_rate  = Column(Float, default=0.0)           # ดอกเบี้ย %
    due_date       = Column(String, nullable=True)        # วันครบกำหนด
    note           = Column(String, nullable=True)
