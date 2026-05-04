from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import date, timedelta
import models, schemas
from database import get_db

router = APIRouter(prefix="/habits", tags=["habits"])


def calc_streak(logs: list[date]) -> int:
    if not logs:
        return 0
    sorted_logs = sorted(set(logs), reverse=True)
    streak = 0
    check = date.today()
    for log_date in sorted_logs:
        if log_date == check:
            streak += 1
            check -= timedelta(days=1)
        else:
            break
    return streak


@router.get("/", response_model=List[schemas.HabitOut])
def list_habits(db: Session = Depends(get_db)):
    habits = db.query(models.Habit).all()
    result = []
    for h in habits:
        log_dates = [hl.date for hl in db.query(models.HabitLog).filter_by(habit_id=h.id).all()]
        result.append(schemas.HabitOut(
            id=h.id, name=h.name, emoji=h.emoji,
            streak=calc_streak(log_dates),
            logs=[str(d) for d in log_dates]
        ))
    return result


@router.post("/", response_model=schemas.HabitOut, status_code=201)
def create_habit(payload: schemas.HabitCreate, db: Session = Depends(get_db)):
    habit = models.Habit(**payload.model_dump())
    db.add(habit)
    db.commit()
    db.refresh(habit)
    return schemas.HabitOut(id=habit.id, name=habit.name, emoji=habit.emoji, streak=0, logs=[])


@router.post("/{habit_id}/log", response_model=schemas.HabitOut)
def log_habit(habit_id: int, payload: schemas.HabitLogCreate, db: Session = Depends(get_db)):
    habit = db.get(models.Habit, habit_id)
    if not habit:
        raise HTTPException(status_code=404, detail="Habit not found")
    existing = db.query(models.HabitLog).filter_by(habit_id=habit_id, date=payload.date).first()
    if not existing:
        db.add(models.HabitLog(habit_id=habit_id, date=payload.date))
        db.commit()
    log_dates = [hl.date for hl in db.query(models.HabitLog).filter_by(habit_id=habit_id).all()]
    return schemas.HabitOut(id=habit.id, name=habit.name, emoji=habit.emoji, streak=calc_streak(log_dates), logs=[str(d) for d in log_dates])


@router.delete("/{habit_id}/log/{log_date}", status_code=204)
def delete_log(habit_id: int, log_date: date, db: Session = Depends(get_db)):
    log = db.query(models.HabitLog).filter_by(habit_id=habit_id, date=log_date).first()
    if log:
        db.delete(log)
        db.commit()
