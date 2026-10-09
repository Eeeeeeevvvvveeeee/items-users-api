from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

import src.models as models
import src.schemas.item as Items
from src.services.crud import perform_action
from src.database import get_db

# router instance
router = APIRouter(
    prefix="/items", 
    tags=["Items"]
)

# Post
@router.post("/", response_model=Items.Item)
def create_item(item: Items.ItemCreate, db: Session = Depends(get_db)):
    return perform_action(method="POST", db=db, model=models.Item, data=item)


#fetch all items
@router.get("/", response_model=list[Items.Item])
def read_items(db: Session = Depends(get_db)):
    return perform_action(method="GET", db=db, model=models.Item)

# Get item by id
@router.get("/{item_id}", response_model=Items.Item)
def read_item(item_id: int, db: Session = Depends(get_db)):
    return perform_action(method="GET", db=db, model=models.Item, id=item_id)

#Put
@router.put("/{item_id}", response_model=Items.Item)
def update_item(item_id: int, item: Items.ItemCreate, db: Session = Depends(get_db)):
    return perform_action(method="PUT", db=db, model=models.Item, data=item, id=item_id)


#delete
@router.delete("/{item_id}")
def delete_item(item_id: int, db: Session = Depends(get_db)):
    return perform_action(method="DELETE", db=db, model=models.Item, id=item_id)