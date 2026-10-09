from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

import model.models as models
import schemas.Users.User as Users
from Database.database import SessionLocal, engine
from routers import items
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="2 API User and Item -Using Postman")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def home():
    return {"message": "API is working"}

app.include_router(items.router)

# User - POST
@app.post("/users/", response_model=Users.User, tags=["Users"])
def create_user(user: Users.UserCreate, db: Session = Depends(get_db)):
    db_user = models.User(
        username=user.username,
        email=user.email,
        is_active=user.is_active,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


# ---------- GET: Fetch all users ----------
@app.get("/users/", response_model=list[Users.User], tags=["Users"])
def read_users(db: Session = Depends(get_db)):
    return db.query(models.User).all()


# ---------- GET: Fetch one user by ID ----------
@app.get("/users/{user_id}", response_model=Users.User, tags=["Users"])
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


# ---------- PUT: Update a user ----------
@app.put("/users/{user_id}", response_model=Users.User, tags=["Users"])
def update_user(user_id: int, user: Users.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    db_user.username = user.username
    db_user.email = user.email
    db_user.is_active = user.is_active

    db.commit()
    db.refresh(db_user)
    return db_user


# ---------- DELETE: Remove a user ----------
@app.delete("/users/{user_id}", tags=["Users"])
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(db_user)
    db.commit()
    return {"message": f"User {user_id} deleted"}