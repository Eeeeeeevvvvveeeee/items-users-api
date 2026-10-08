from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

import models
import schemas
from database import SessionLocal, engine

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

# Item - POST
@app.post("/items/", response_model=schemas.Item,tags=["Items"])
def create_item(item: schemas.ItemCreate, db: Session = Depends(get_db)):
    db_item = models.Item(
        name=item.name,
        description=item.description,
        is_offer=item.is_offer
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

#Fetch all items
@app.get("/items/", response_model=list[schemas.Item], tags=["Items"])
def read_items(db: Session = Depends(get_db)):
    items = db.query(models.Item).all()
    return items

#Get one item by id
@app.get("/items/{item_id}", response_model=schemas.Item,tags=["Items"])
def read_item(item_id: int, db: Session = Depends(get_db)):
    db_item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item

#Put
@app.put("/items/{item_id}", response_model=schemas.Item,tags=["Items"])
def update_item(item_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)):
    db_item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")

    db_item.name = item.name
    db_item.description = item.description
    db_item.is_offer = item.is_offer

    db.commit()
    db.refresh(db_item)
    return db_item

#Delete
@app.delete("/items/{item_id}",tags=["Items"])
def delete_item(item_id: int, db: Session = Depends(get_db)):
    db_item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")

    db.delete(db_item)
    db.commit()
    return {"message": f"Item {item_id} deleted"}


# User - POST
@app.post("/users/", response_model=schemas.User, tags=["Users"])
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
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
@app.get("/users/", response_model=list[schemas.User], tags=["Users"])
def read_users(db: Session = Depends(get_db)):
    return db.query(models.User).all()


# ---------- GET: Fetch one user by ID ----------
@app.get("/users/{user_id}", response_model=schemas.User, tags=["Users"])
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


# ---------- PUT: Update a user ----------
@app.put("/users/{user_id}", response_model=schemas.User, tags=["Users"])
def update_user(user_id: int, user: schemas.UserCreate, db: Session = Depends(get_db)):
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