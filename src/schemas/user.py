from pydantic import BaseModel

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