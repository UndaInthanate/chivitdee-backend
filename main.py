from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import Base, engine
import models
from routers import budget, expense, savings, habits, debt, scan, income

Base.metadata.create_all(bind=engine)

app = FastAPI(title="ชีวิตดี API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(budget.router)
app.include_router(expense.router)
app.include_router(savings.router)
app.include_router(habits.router)
app.include_router(debt.router)
app.include_router(scan.router)
app.include_router(income.router)


@app.get("/")
def root():
    return {"message": "ชีวิตดี API is running 🌿"}
