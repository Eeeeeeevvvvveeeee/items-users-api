from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src import models
import src.schemas.user as Users
from src.services.crud import perform_action
from src.database import get_db


router = APIRouter(prefix="/users", tags=["Users"])

#POST
@router.post("/", response_model=Users.User)
def create_user(user: Users.UserCreate, db: Session = Depends(get_db)):
    return perform_action(method="POST", db=db, model=models.User, data=user)


# Fetch
@router.get("/", response_model=list[Users.User])
def read_users(db: Session = Depends(get_db)):
    return perform_action(method="GET", db=db, model=models.User)


# GET
@router.get("/{user_id}", response_model=Users.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    return perform_action(method="GET", db=db, model=models.User, id=user_id)


#PUT
@router.put("/{user_id}", response_model=Users.User)
def update_user(user_id: int, user: Users.UserCreate, db: Session = Depends(get_db)):
    return perform_action(method="PUT", db=db, model=models.User, data=user, id=user_id)


# DELETE
@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    return perform_action(method="DELETE", db=db, model=models.User, id=user_id)