
"""
Utility functions
"""

from passlib.context import CryptContext
from sqlalchemy.orm import Session

import models
import schemas

# utility functions for hashing password and etc
# iniitialization step for hashing algorithms
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")



# From fastapi tutorial 2023/10/5
def verify_password(plain_password, hashed_password):
    """
    Verify that the password, after hashing, matches the hashed password
    :param plain_password  Plain text password
    :param hashed_password  Hashed password
    :returns: True if passwords match
    """
    return pwd_context.verify(plain_password, hashed_password)

# From fastapi tutorial 2023/10/5
def get_password_hash(password: str):
    """
    Hash the password

    :param password: Plain text passwor
    :returns: hashed password
    """
    return pwd_context.hash(password)

# From https://fastapi.tiangolo.com/tutorial/sql-databases/ 2023/10/6
def get_user(db: Session, username: str):
    """
    Get user information from database
    :param db: database
    :param user_id:  User id
    """
    return db.query(models.User).filter(models.User.username == username).first()

# From fastapi tutorial 2023/09/18
# def get_user(db, username: str):
#     """
#     Return user info if username is found in user database

#     :param db: database with user info
#     :param username: username
#     :returns: user info if username found, else nothing
#     """
#     if username in db:
#         user_dict = db[username]
#         return schemas.UserInDB(**user_dict)

# From https://fastapi.tiangolo.com/tutorial/sql-databases/ 2023/10/6
def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

# From https://fastapi.tiangolo.com/tutorial/sql-databases/ 2023/10/6
def get_users(db: Session, skip: int=0, limit: int=100):
    return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas.UserCreate):
    # Create a SQLAlchemy model instance with your data
    # add that instance object to your database session
    # commit the changes to the database so they are saved
    # refresh the instance so it contains any new data from 
    # the database, like the generated ID

    hashed_password = get_password_hash(user.password)
    db_user = models.User(
        email=user.email,
        username=user.username,
        hashed_password=hashed_password,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_items(db: Session, skip: int=0, limit: int=100):
    return db.query(models.Item).offset(skip).limit(limit).all()

def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
    db_item = models.Item(**item.dict(), owner=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def authenticate_user(fake_db, username: str, password: str):
    """
    Authenticate and return a user
    
    :param fake_db: For now, a fake database of user info
    :param username: The username
    :param password: The password, to be verified
    :returns: user  The user info from the fake database
    """
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user
