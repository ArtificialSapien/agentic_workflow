from contextlib import asynccontextmanager
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
from fastapi import APIRouter, Depends, FastAPI, HTTPException, Query, Security, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer, HTTPBasic, SecurityScopes
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
from pydantic import BaseModel, ValidationError
from sqlmodel import Field, Session, SQLModel, create_engine, select
from typing import Annotated

import jwt
import os

# Load environment variables
load_dotenv(override=True)

SECRET_KEY = os.getenv("AS_APP_JWT_SECRET_KEY")
ALGORITHM = os.getenv("AS_APP_JWT_ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("AS_APP_JWT_ACCESS_TOKEN_EXPIRE_MINUTES"))
DB_URL = os.getenv("AS_APP_DB_URL")
REQUEST_LIMIT = int(os.getenv("AS_APP_REQUEST_LIMIT"))


security = HTTPBasic()
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="token",
    scopes={"all": "Use the app with all its functionalities."}
)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserBase(SQLModel):
    username: str = Field(index=True, unique=True)


class User(UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    password: str = Field(index=True)
    disabled: bool = Field(default=False)
    number_of_queries: int = Field(default=0)
    scopes: str = Field(default="all")


class UserPublic(UserBase):
    id: int
    scopes: str
    number_of_queries: int


class UserCreate(UserBase):
    password: str


class UserUpdate(UserBase):
    username: str | None = None
    password: str | None = None


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: (str | None) = None
    scopes: list[str] = []


def verify_password(plain_password, hashed_password) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password) -> str:
    return pwd_context.hash(password)


def authenticate_user(username: str, password: str):
    user = user_repo.get_by_username(username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(security_scopes: SecurityScopes, token: Annotated[str, Depends(oauth2_scheme)]):
    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
    else:
        authenticate_value = "Bearer"
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": authenticate_value},
    )
    try:
        # Todo: Catch exception if incorrect algo or key is provided
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_scopes = payload.get("scopes", [])
        if type(token_scopes) == str:  # Todo: That should be prettier
            token_scopes = [token_scopes]
        token_data = TokenData(scopes=token_scopes, username=username)
    except (InvalidTokenError, ValidationError) as e:
        raise credentials_exception
    user = user_repo.get_by_username(username=token_data.username)
    if user is None:
        raise credentials_exception
    for scope in security_scopes.scopes:
        if scope not in token_data.scopes:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not enough permissions",
                headers={"WWW-Authenticate": authenticate_value},
            )
    return user


async def get_current_active_user(current_user: Annotated[User, Security(get_current_user, scopes=["all"])]):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


class UserRepoUsingSQLModelPackage:
    def __init__(self, db_url="sqlite:///local.db", connect_args=None):
        db_type = db_url.split(':')[0].lower()
        if db_type == 'sqlite':
            connect_args = {"check_same_thread": False}
        self.engine = create_engine(db_url, connect_args=connect_args)

    def get_by_username(self, username: str) -> User | None:
        statement = select(User).where(User.username == username)
        user = Session(self.engine).exec(statement).one()
        return user


class UserRepoInMemory:
    def __init__(self):
        self.__repo: dict[int, User] = {}

    def exists(self, user_id: int) -> bool:
        return user_id in self.__repo.keys()

    def exists_by_name(self, username: str) -> bool:
        for user in self.__repo.values():
            if user.username == username:
                return True
        return False

    def add(self, user: User) -> None:
        self.__repo[user.id] = user

    def get(self, user_id: int) -> User | None:
        if user_id in self.__repo:
            return self.__repo[user_id]
        return None

    def get_by_username(self, username: str) -> User | None:
        for user in self.__repo.values():
            if user.username == username:
                return user
        return None

    def get_all(self) -> dict[int, User]:
        return self.__repo

    def delete_by_id(self, user_id: int) -> None:
        if user_id in self.__repo:
            self.__repo.pop(user_id)


# user_repo = UserRepoInMemory()
user_repo = UserRepoUsingSQLModelPackage(DB_URL)


def create_db_and_tables():
    SQLModel.metadata.create_all(user_repo.engine)


def get_session():
    with Session(user_repo.engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]


@asynccontextmanager
async def lifespan(app: FastAPI):
    # On startup
    create_db_and_tables()

    yield
    # On shutdown


router = APIRouter(lifespan=lifespan)


@router.post("/token", tags=["Users"])
async def login_for_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], session: SessionDep) -> Token:
    user = user_repo.get_by_username(form_data.username)
    login_fails = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="Incorrect username or password",
                                headers={"WWW-Authenticate": "Bearer"},
                                )
    if not user:
        raise login_fails
    if not verify_password(form_data.password, user.password):
        raise login_fails

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username, "scopes": user.scopes}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


@router.post("/users", response_model=UserPublic, tags=["Users"])
def create_user(user: UserCreate, session: SessionDep) -> User:
    # New users can only be created by a user with `admin` scope
    # Where to create a user id?
    #
    # Workflow
    # * Check that current_user has valid token and is admin
    # * Check that new_username does not exist yet
    # * Check that password is strong enough
    try:
        db_user = User.model_validate(user)
        db_user.password = get_password_hash(db_user.password)
        session.add(db_user)
        session.commit()
        session.refresh(db_user)
        return db_user
    except Exception as e:
        raise HTTPException(status_code=404, detail="User exists.")


@router.get("/users", response_model=list[UserPublic], tags=["Users"])
def read_users(current_user: Annotated[User, Security(get_current_active_user, scopes=["all"])],
               session: SessionDep,
               offset: int = 0,
               limit: Annotated[int, Query(le=100)] = 100,
               ) -> list[User]:
    users = session.exec(select(User).offset(offset).limit(limit)).all()
    return users


def increment_usage_count(session, username: str) -> int:
    statement = select(User).where(User.username == username)
    results = session.exec(statement)
    user = results.one()

    user.number_of_queries += 1
    session.add(user)
    session.commit()
    session.refresh(user)

    return user.number_of_queries




@router.get("/info", tags=["Users"])
def get_info(current_user: Annotated[User, Security(get_current_active_user, scopes=["all"])], session: SessionDep):
    number_of_requests = increment_usage_count(session, current_user.username)
    remaining_requests = REQUEST_LIMIT - number_of_requests
    if remaining_requests > 0:
        return {"user": current_user.username, "remaining_requests": remaining_requests}
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You ran out of requests")


@router.get("/users/me", tags=["Users"])
async def read_users_me(current_user: Annotated[User, Security(get_current_active_user, scopes=["all"])]):
    return current_user
