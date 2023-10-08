from database import Base
from sqlalchemy import Column, Integer, String, Boolean, Float, ForeignKey
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    # email = Column(String, unique=True, index=True)
    
    # When accessing my_user.items, SQLAlchemy will fetch the items 
    # from the items table and populate them here.
    # items = relationship("Item", back_populates="owner")

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))

    # When accessing the attribute owner in an Item, will 
    # use the owner_id attribute/column with its foreign 
    # key to know which record to get from the users table.
    # owner = relationship("User", back_populates="items")

class Shares(Base):
    """Plant shares"""
    __tablename__ = "shares"

    id = Column(Integer, primary_key=True, index=True)
    plant_name = Column(String)
    shared_by = Column(String)
    amount = Column(Float)
    description = Column(String)
    is_available_now = Column(Boolean)
    date = Column(String)


class Requests(Base):
    """Plant requests"""
    __tablename__ = "requests"

    id = Column(Integer, primary_key=True, index=True)
    plant_name = Column(String)
    requested_by = Column(String)
    amount = Column(Float)
    notes = Column(String)
    date = Column(String)

