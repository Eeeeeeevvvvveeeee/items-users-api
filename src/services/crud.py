from fastapi import HTTPException
from sqlalchemy.orm import Session


ALLOWED_METHODS = {"POST", "GET", "PUT", "DELETE"}

def _create(db: Session, model, data, pre_save=None):
    payload = data.model_dump()
    if pre_save is not None:
        payload = pre_save(payload)

    db_item = model(**payload)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def _read_all(db: Session, model):
    return db.query(model).all()

def _read_one(db: Session, model, id: int):
    db_item = db.query(model).filter(model.id == id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail=f"{model.__name__} not found")
    return db_item

def _update(db: Session, model, id: int, data, pre_save=None):
    db_item = db.query(model).filter(model.id == id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail=f"{model.__name__} not found")

    payload = data.model_dump()

    if pre_save is not None:
        payload = pre_save(payload)

    for field, value in payload.items():
        setattr(db_item, field, value)

    db.commit()
    db.refresh(db_item)
    return db_item

def _delete(db: Session, model, id: int):
    db_item = db.query(model).filter(model.id == id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail=f"{model.__name__} not found")

    db.delete(db_item)
    db.commit()
    return {"message": f"{model.__name__} {id} deleted"}

def perform_action(
    method: str,
    db: Session,
    model,
    data=None,
    id: int = None,
    pre_save=None,
):
    if method not in ALLOWED_METHODS:
        raise ValueError(
            f"Unsupported method '{method}'. "
            f"Allowed: {sorted(ALLOWED_METHODS)}"
        )

   #POST
    if method == "POST":
        if data is None:
            raise ValueError("POST requires 'data'")
        return _create(db, model, data, pre_save=pre_save)

    #Fetch
    if method == "GET":
        if id is None:
            return _read_all(db, model)
        return _read_one(db, model, id)

    # PUT
    if method == "PUT":
        if data is None or id is None:
            raise ValueError("PUT requires both 'data' and 'id'")
        return _update(db, model, id, data, pre_save=pre_save)

    #DELETE
    if method == "DELETE":
        if id is None:
            raise ValueError("DELETE requires 'id'")
        return _delete(db, model, id)