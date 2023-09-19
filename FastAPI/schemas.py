from pydantic import BaseModel
from typing import Annotated, Union
from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordBearer


# From fastapi tutorial
class User(BaseModel):
    username: str
    email: Union[str, None] = None
    full_name: Union[str, None] = None
    disabled: Union[bool, None] = None


# From fastapi tutorial 2023/09/18
class UserInDB(User):
    hashed_password: str


class ShareBase(BaseModel):
    """Pydantic model that accepts or regects plant share"""

    plant_name: str
    shared_by: str
    amount: float
    description: str
    is_available_now: bool
    date: str


class ShareModel(ShareBase):
    """
    The model for sharing
    """

    id: int

    class Config:
        from_attributes = True
