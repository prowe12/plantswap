from database import Base
from sqlalchemy import Column, Integer, String, Boolean, Float


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

