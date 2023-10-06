"""
Plant Swap App using FastAPI, React, and SQLAlchemy

Penny M. Rowe

Acknowledgements:
https://www.youtube.com/watch?v=0zb2kohYZIM
https://developer.mozilla.org/en-US/docs/Learn/Tools_and_testing/Client-side_JavaScript_frameworks/React_getting_started
https://fastapi.tiangolo.com/tutorial/
https://betterprogramming.pub/how-to-authentication-users-with-token-in-a-react-application-f99997c2ee9d
https://www.youtube.com/watch?v=_dIs3IZAG0Q
Daniel Neshyba-Rowe
"""

from datetime import datetime, timedelta
from typing import Annotated, List
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from database import SessionLocal, engine

from schemas import User, UserInDB, ShareBase, ShareModel, RequestBase, RequestModel, Token, TokenData
import models

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "00972ba440d93ae95db349c7ccd03d61f3a7138a4a14fae93402edd73db9a05b"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


# From fastapi tutorial 2023/09/18
fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW", # secret
        "disabled": False,
    },
}



app = FastAPI()


# Middleware
# TODO: Maybe the token one is not needed
origins = [
    "http://localhost:8000",
    "http://localhost:8000/token",
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# utility functions for hashing password and etc
# iniitialization step for hashing algorithms
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Use OAuth2, with the Password flow, using a Bearer token, using the
# OAuth2PasswordBearer class. tokenUrl="token" refers to a relative
# URL token, equivalent to ./token. This parameter declares that the
# URL /token will be the one that the client should use to get the token.
# That information is used in OpenAPI, and then in the interactive
# API documentation systems. The oauth2_scheme variable is an instance
# of OAuth2PasswordBearer, but it is also a "callable".
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


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

# From fastapi tutorial 2023/09/18
def get_user(db, username: str):
    """
    Return user info if username is found in user database
    
    :param db: database with user info
    :param username: username
    :returns: user info if username found, else nothing
    """
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


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

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    """
    Utility function for generating a new access token
    
    :param data: JWT specification data
    :param expires_delta: Time until token expires
    :returns: encoded_jwt
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_db():
    """
    Dependency injection for our plant shares database. Only opens when
    request comes in and closes when request is complete
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_requests_db():
    """
    Dependency injection for our plant requests database. Only opens when
    request comes in and closes when request is complete
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create database which will create table with columns automatically
# Set a variable to contain the type. Here Depends tells fastapi
# that this type is something that a function may need but not
# something it will get from a user submitting to an endpoint
db_dependency = Annotated[Session, Depends(get_db)]
db_dependency_requests = Annotated[Session, Depends(get_requests_db)]
token_dependency = Annotated[str, Depends(oauth2_scheme)]

models.Base.metadata.create_all(bind=engine)


# Create endpoint for shares
# Because db is type that has Depends in it, the user will not need
# to specifiy it
@app.post("/shares/", response_model=ShareModel)
async def create_share(share: ShareBase, db: db_dependency):
    """
    Shares endpoint: Map variables from ShareBase to share table to save 
    into sqlite database
    
    :params share: Info posted to shares endpoint from frontend
    :params db: database to add shares to
    :returns: db_share
    """
    # , token: token_dependency)
    # model_dump() generates a dictionary representation of the model
    # ** performs a dictionary decomposition
    db_share = models.Shares(**share.dict())
    # .dict() is deprecated; try the following instead:
    # db_share = models.Shares(**share.model_dump())
    db.add(db_share)
    db.commit()
    db.refresh(db_share)
    return db_share


@app.get(
    "/shares/",
    response_model=List[ShareModel],
)
async def read_shares(db: db_dependency):
    """
    Get the shared plants
    
    :param db: The database that has the shares to get
    :returns: The shares info from the database
    """
    # token: token_dependency,
    shares = db.query(models.Shares).all()
    return shares



@app.delete("/shares/{shares_id}")
async def delete_share(shares_id: int, db: Session = Depends(get_db)):
    """
    Delete a shared plant from the database
    
    :param shares_id: Id of plant to be deleted
    :param db: Database of shared plants
    :returns:  Successful response if successful
    :raises  HTTPException if unsuccessful
    """
    query_result = db.query(models.Shares).filter(models.Shares.id == shares_id).first()

    if query_result is None:
        raise HTTPException(status_code=404, detail="Plant not found in shares")

    db.query(models.Shares).filter(models.Shares.id == shares_id).delete()
    db.commit()

    return successful_response(200)


def successful_response(status_code: int):
    """
    Return status code and successful transaction
    
    :param status_code: The desired status code
    :returns: status code and successful transaction 
    """
    return {"status": status_code, "transaction": "Successful"}


# Create endpoint for plant requests
@app.post("/requests/", response_model=RequestModel)
async def create_request(request: RequestBase, db: db_dependency_requests):
    """
    Map the variables from our RequestBase to our requests table to
    save into our sqlite database
    """
    db_request = models.Requests(**request.dict())
    db.add(db_request)
    db.commit()
    db.refresh(db_request)
    return db_request


@app.get(
    "/requests/",
    response_model=List[RequestModel],
)
async def read_requests(db: db_dependency_requests):
    """Get the requested plant"""
    requests = db.query(models.Requests).all()
    return requests



@app.delete("/requests/{requests_id}")
async def delete_request(requests_id: int, db: Session = Depends(get_requests_db)):
    """Delete a shared plant from the database"""
    request_model = db.query(models.Requests).filter(models.Requests.id == requests_id).first()

    if request_model is None:
        raise HTTPException(status_code=404, detail="Plant not found in requests")

    db.query(models.Requests).filter(models.Requests.id == requests_id).delete()
    db.commit()

    return successful_response(200)


# From fastapi tutorial; updated 2023/10/05
# The dependency below will provide a str that is assigned to the parameter
# token of the path operation function.
async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    """
    Get the user corresponding to the input token
    :param token: The token
    :returns: User info corresponding to the username from the input token
    :raises credentials_exception if username missing from token or user not in database
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(fake_users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

# From fastapi tutorial 2023/09/18
# Want to get the current_user only if they exist, was correctly authenticated, and
# is active (i.e. not disabled). For the latter, we need an additional dependency
# that in turn uses get_current_user as a dependency.
async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)]
):
    """
    Get the user for the token if they are active

    :param current_user:  The current user; from dependency
    :returns:  The user info
    :raises  HTTPException if the current user is disabled (not active)
    """
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


# From fastapi tutorial 2023/09/18
# Use OAuth2PasswordRequestForm as a dependency with Depends in the path
# operation for /token. OAuth2PasswordRequestForm is a class dependency (???)
# that declares a form body with:
# The username.
# The password.
# An optional scope field as a big string, composed of strings separated by spaces.
# An optional grant_type.
@app.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    """
    Return access token for username and password given in form data if authenticated
    
    :param form_data: Login info from frontend
    :returns: Access token
    :raises  HTTPException if authentication fails
    """
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    # The JWT specification includes key sub, with the subject of the token.
    # sub (which is optional) is where to put user's identification
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

# @app.post("/token")
# async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
#     # Get the user data from the (fake) database, using the username from
#     # the form field. If there is no such user, return an error saying
#     # "incorrect username or password". For the error, use the exception HTTPException:
#     user_dict = fake_users_db.get(form_data.username)
#     if not user_dict:
#         raise HTTPException(status_code=400, detail="Incorrect username or password")
#     # Put the data in the UserInDB model. Recall that fake_users_db, and thus user_dict
#     # has the fields username, full_name, email, hashed_password, fakehashedsecret
#     # and disabled, for two people. Here we just get the info for form_data.username
#     # Recall that **user_dict means pass the keys and values of the user_dict directly
#     # as key-value arguments
#     user = UserInDB(**user_dict)
#     # Check that the hash of the password from the form matches the pasword from
#     # the (fake) database.
#     hashed_password = fake_hash_password(form_data.password)
#     if not hashed_password == user.hashed_password:
#         raise HTTPException(status_code=400, detail="Incorrect username or password")
#     # The response of the token endpoint must be a JSON object. It should have a token_type.
#     # Here, we are using "Bearer" tokens, so the token type should be "bearer". And
#     # it should have an access_token, with a string containing our access token.
#     # Here, we are returning the same username as the token, which is not secure.
#     return {"access_token": user.username, "token_type": "bearer"}


# From fastapi tutorial; updated 2023/09/18
# Below, current_user is not coming in as a get parameter, but rather
# from the dependency get_current_active_user
@app.get("/users/me/", response_model=User)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    """
    Return the user info for the current user

    :param current_user:  User info; from dependency
    :returns:  User info
    """
    return current_user


# TODO: Probably will not use this
@app.get("/users/me/items/")
async def read_own_items(
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    """
    Return items from a users endpoint

    :params current_user: User info; from dependency
    :returns:  User items
    """
    return [{"item_id": "Foo", "owner": current_user.username}]


