"""
Plant Swap App using FastAPI, React, and SQLAlchemy

Penny M. Rowe

Acknowledgements:
https://www.youtube.com/watch?v=0zb2kohYZIM
https://developer.mozilla.org/en-US/docs/Learn/Tools_and_testing/Client-side_JavaScript_frameworks/React_getting_started
https://fastapi.tiangolo.com/tutorial/
https://betterprogramming.pub/how-to-authentication-users-with-token-in-a-react-application-f99997c2ee9d
https://www.youtube.com/watch?v=_dIs3IZAG0Q
"""

from typing import Annotated, List
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from database import SessionLocal, engine

from schemas import User, UserInDB, ShareBase, ShareModel, RequestBase, RequestModel
import models


# From fastapi tutorial 2023/09/18
fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "fakehashedsecret",
        "disabled": False,
    },
    "alice": {
        "username": "alice",
        "full_name": "Alice Wonderson",
        "email": "alice@example.com",
        "hashed_password": "fakehashedsecret2",
        "disabled": True,
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


# From fastapi tutorial 2023/09/18
def fake_hash_password(password: str):
    return "fakehashed" + password


# Use OAuth2, with the Password flow, using a Bearer token, using the
# OAuth2PasswordBearer class. tokenUrl="token" refers to a relative
# URL token, equivalent to ./token. This parameter declares that the
# URL /token will be the one that the client should use to get the token.
# That information is used in OpenAPI, and then in the interactive
# API documentation systems. The oauth2_scheme variable is an instance
# of OAuth2PasswordBearer, but it is also a "callable".
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# From fastapi tutorial 2023/09/18
def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


# From fastapi tutorial; updated 2023/09/18
# This is a fake utility because in action it would get the user corresponding to the
# token from, e.g. a database
def fake_decode_token(token):
    # This doesn't provide any security at all
    # Check the next version
    user = get_user(fake_users_db, token)
    return user


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
    Map the variables from our ShareBase to our share table to
    save into our sqlite database
    """
    # , token: token_dependency)
    # Note: the ** below is a dictionary decomposition
    db_share = models.Shares(**share.dict())
    db.add(db_share)
    db.commit()
    db.refresh(db_share)
    return db_share


@app.get(
    "/shares/",
    response_model=List[ShareModel],
)
async def read_shares(db: db_dependency):
    """Get the shared plants"""
    # token: token_dependency,
    shares = db.query(models.Shares).all()
    return shares


def http_exception():
    return HTTPException(status_code=404, detail="Plant not found")


@app.delete("/shares/{shares_id}")
async def delete_share(shares_id: int, db: Session = Depends(get_db)):
    """Delete a shared plant from the database"""
    todo_model = db.query(models.Shares).filter(models.Shares.id == shares_id).first()

    if todo_model is None:
        raise http_exception()

    db.query(models.Shares).filter(models.Shares.id == shares_id).delete()
    db.commit()

    return successful_response(200)


def successful_response(status_code: int):
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
        raise http_exception()

    db.query(models.Requests).filter(models.Requests.id == requests_id).delete()
    db.commit()

    return successful_response(200)


# From fastapi tutorial; updated 2023/09/18
# The dependency below will provide a str that is assigned to the parameter
# token of the path operation function.
async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    user = fake_decode_token(token)
    if not user:
        # Any HTTP (error) status code 401 "UNAUTHORIZED" should return a WWW-Authenticate
        # header. For bearer tokens, the value of that header should be Bearer.
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate:" "Bearer"},
        )
    return user


# From fastapi tutorial 2023/09/18
# Want to get the current_user only if they exist, was correctly authenticated, and
# is active (i.e. not disabled). For the latter, we need an additional dependency
# that in turn uses get_current_user as a dependency.
async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)]
):
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
@app.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    # Get the user data from the (fake) database, using the username from
    # the form field. If there is no such user, return an error saying
    # "incorrect username or password". For the error, use the exception HTTPException:
    user_dict = fake_users_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    # Put the data in the UserInDB model. Recall that fake_users_db, and thus user_dict
    # has the fields username, full_name, email, hashed_password, fakehashedsecret
    # and disabled, for two people. Here we just get the info for form_data.username
    # Recall that **user_dict means pass the keys and values of the user_dict directly
    # as key-value arguments
    user = UserInDB(**user_dict)
    # Check that the hash of the password from the form matches the pasword from
    # the (fake) database.
    hashed_password = fake_hash_password(form_data.password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    # The response of the token endpoint must be a JSON object. It should have a token_type.
    # Here, we are using "Bearer" tokens, so the token type should be "bearer". And
    # it should have an access_token, with a string containing our access token.
    # Here, we are returning the same username as the token, which is not secure.
    return {"access_token": user.username, "token_type": "bearer"}


# From fastapi tutorial; updated 2023/09/18
# Below, current_user is not coming in as a get parameter, but rather
# from the dependency get_current_active_user
@app.get("/users/me")
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    return current_user
