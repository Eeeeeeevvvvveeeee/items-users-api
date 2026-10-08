from pydantic import BaseModel

class ItemBase(BaseModel):
    name: str
    description: str | None = None
    is_offer: bool | None = None


class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    id: int

    class Config:
        from_attributes = True

class UserBase(BaseModel):
    username: str
    email: str
    is_active: bool | None = True


class UserCreate(UserBase):
    pass


class User(UserBase):
    id: int

    class Config:
        from_attributes = True