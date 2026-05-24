from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from sqlalchemy import func
import datetime
from typing import List, Optional

import database, models, schemas

app = FastAPI(title="Team Standup Tracker")

# Create tables
database.init_db()

# Dependency
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# API Endpoints

@app.post("/members/", response_model=schemas.TeamMember)
def create_member(member: schemas.TeamMemberCreate, db: Session = Depends(get_db)):
    db_member = models.TeamMember(name=member.name)
    db.add(db_member)
    try:
        db.commit()
        db.refresh(db_member)
    except Exception:
        db.rollback()
        raise HTTPException(status_code=400, detail="Member already exists")
    return db_member

@app.get("/members/", response_model=List[schemas.TeamMember])
def read_members(db: Session = Depends(get_db)):
    return db.query(models.TeamMember).all()

@app.post("/updates/", response_model=schemas.StandupUpdate)
def create_update(update: schemas.StandupUpdateCreate, db: Session = Depends(get_db)):
    db_update = models.StandupUpdate(**update.dict())
    db.add(db_update)
    db.commit()
    db.refresh(db_update)
    return db_update

@app.get("/dashboard/")
def get_dashboard(db: Session = Depends(get_db)):
    # Get latest update for each member
    subquery = db.query(
        models.StandupUpdate.member_id,
        func.max(models.StandupUpdate.created_at).label("max_created")
    ).group_by(models.StandupUpdate.member_id).subquery()

    latest_updates = db.query(models.StandupUpdate).join(
        subquery,
        (models.StandupUpdate.member_id == subquery.c.member_id) &
        (models.StandupUpdate.created_at == subquery.c.max_created)
    ).all()

    # Get active blockers (those from the latest updates that are not null or empty)
    blockers = [u for u in latest_updates if u.blockers and u.blockers.strip()]

    return {
        "latest_updates": latest_updates,
        "active_blockers": blockers
    }

@app.get("/search/")
def search_updates(q: str = Query(...), db: Session = Depends(get_db)):
    # Search in working_on or blockers
    results = db.query(models.StandupUpdate).filter(
        (models.StandupUpdate.working_on.ilike(f"%{q}%")) |
        (models.StandupUpdate.blockers.ilike(f"%{q}%"))
    ).order_by(models.StandupUpdate.created_at.desc()).all()
    
    # Also return member name with update
    output = []
    for r in results:
        output.append({
            "id": r.id,
            "member_name": r.member.name,
            "working_on": r.working_on,
            "status": r.status,
            "blockers": r.blockers,
            "created_at": r.created_at
        })
    return output

@app.get("/report/")
def get_report(start_date: str = None, end_date: str = None, db: Session = Depends(get_db)):
    # Period-based summary report
    today = datetime.date.today()
    if not start_date:
        start_date_dt = datetime.datetime.combine(today, datetime.time.min)
    else:
        start_date_dt = datetime.datetime.strptime(start_date, "%Y-%m-%d")
    
    if not end_date:
        end_date_dt = datetime.datetime.combine(today, datetime.time.max)
    else:
        end_date_dt = datetime.datetime.strptime(end_date, "%Y-%m-%d") + datetime.timedelta(days=1)

    updates = db.query(models.StandupUpdate).filter(
        models.StandupUpdate.created_at >= start_date_dt,
        models.StandupUpdate.created_at < end_date_dt
    ).all()

    all_members = db.query(models.TeamMember).all()
    posted_today_ids = {u.member_id for u in updates if u.created_at.date() == today}
    
    who_posted = [m.name for m in all_members if m.id in posted_today_ids]
    who_did_not_post = [m.name for m in all_members if m.id not in posted_today_ids]

    summary = {
        "completed": [u.working_on for u in updates if "done" in u.status.lower() or "completed" in u.status.lower()],
        "who_posted_today": who_posted,
        "who_did_not_post_today": who_did_not_post,
        "all_updates_in_period": updates
    }
    return summary

import os

# Get the directory of the current script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Serve static files
app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")

@app.get("/", response_class=HTMLResponse)
async def read_index():
    with open(os.path.join(BASE_DIR, "static", "index.html"), encoding="utf-8") as f:
        return f.read()
