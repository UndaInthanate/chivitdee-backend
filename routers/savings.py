from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import models, schemas
from database import get_db

router = APIRouter(prefix="/savings", tags=["savings"])


@router.get("/", response_model=List[schemas.SavingsGoalOut])
def list_goals(db: Session = Depends(get_db)):
    return db.query(models.SavingsGoal).all()


@router.post("/", response_model=schemas.SavingsGoalOut, status_code=201)
def create_goal(payload: schemas.SavingsGoalCreate, db: Session = Depends(get_db)):
    goal = models.SavingsGoal(**payload.model_dump())
    db.add(goal)
    db.commit()
    db.refresh(goal)
    return goal


@router.put("/{goal_id}", response_model=schemas.SavingsGoalOut)
def update_goal(goal_id: int, payload: schemas.SavingsGoalUpdate, db: Session = Depends(get_db)):
    goal = db.get(models.SavingsGoal, goal_id)
    if not goal:
        raise HTTPException(status_code=404, detail="Goal not found")
    for k, v in payload.model_dump(exclude_none=True).items():
        setattr(goal, k, v)
    db.commit()
    db.refresh(goal)
    return goal


@router.delete("/{goal_id}", status_code=204)
def delete_goal(goal_id: int, db: Session = Depends(get_db)):
    goal = db.get(models.SavingsGoal, goal_id)
    if not goal:
        raise HTTPException(status_code=404, detail="Goal not found")
    db.delete(goal)
    db.commit()
