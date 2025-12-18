from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app.database import Base, engine, SessionLocal
from app import crud, schemas

Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI + PostgreSQL!"}

@app.post("/users/", response_model=schemas.UserRead)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db, user)

@app.get("/users/", response_model=list[schemas.UserRead])
def read_users(db: Session = Depends(get_db)):
    return crud.get_users(db)
