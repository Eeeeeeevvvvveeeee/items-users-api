from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import model.models as models
import schemas.Users.User as Users
from Database.database import SessionLocal

# 1. Create the router instance
router = APIRouter(
    prefix="/items",  # This replaces /items/ in every route below
    tags=["Items"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Post
@router.post("/", response_model=Users.Item)
def create_item(item: Users.ItemCreate, db: Session = Depends(get_db)):
    db_item = models.Item(
        name=item.name,
        description=item.description,
        is_offer=item.is_offer
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


#fetch all items
@router.get("/", response_model=list[Users.Item])
def read_items(db: Session = Depends(get_db)):
    items = db.query(models.Item).all()
    return items

# Get item by id
@router.get("/{item_id}", response_model=Users.Item)
def read_item(item_id: int, db: Session = Depends(get_db)):
    db_item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item

#Put
@router.put("/{item_id}", response_model=Users.Item)
def update_item(item_id: int, item: Users.ItemCreate, db: Session = Depends(get_db)):
    db_item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")

    db_item.name = item.name
    db_item.description = item.description
    db_item.is_offer = item.is_offer

    db.commit()
    db.refresh(db_item)
    return db_item

#delete
@router.delete("/{item_id}")
def delete_item(item_id: int, db: Session = Depends(get_db)):
    db_item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")

    db.delete(db_item)
    db.commit()
    return {"message": f"Item {item_id} deleted"}