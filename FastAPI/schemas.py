"""
Schemas for databases for user login and plant shares
"""

from typing import Union
from pydantic import BaseModel


# From fastapi tutorial


# From fastapi tutorial 2023/10/5
class Token(BaseModel):
    """Model for access tokens"""
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None

class ItemBase(BaseModel):
    title:str
    description: str | None = None

class ItemCreate(ItemBase):
    pass

class Item(ItemBase):
    id: int
    owner_id: int
    
    # Read the data even if it's not a dict but an ORM. The Pydantic 
    # model is then compatible with ORMs, and can be declared in the 
    # response_model argument in the path operations.
    class Config:
        orm_mode = True

class UserBase(BaseModel):
    email: str
    username: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool
    # item: list[Item] = []

    class Config:
        orm_mode = True


# class User(BaseModel):
#     """
#     For managing user logins
#     disabled refers to whether the account is active
#     """

#     username: str
#     email: str | None = None
#     full_name: str | None = None
#     disabled: bool | None = None


# From fastapi tutorial 2023/09/18
class UserInDB(User):
    hashed_password: str


class ShareBase(BaseModel):
    """Pydantic model for plant share"""

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


class RequestBase(BaseModel):
    """Pydantic model for plant request"""

    plant_name: str
    requested_by: str
    amount: float
    notes: str
    date: str


class RequestModel(RequestBase):
    """
    The model for requesting a plant
    """

    id: int

    class Config:
        from_attributes = True
