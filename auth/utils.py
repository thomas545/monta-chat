import os
from typing import Annotated
from jose import JWTError, jwt
from dotenv import load_dotenv
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from .schemas import User, UserResponse

load_dotenv()

SECRET_KEY = os.environ.get("SECRET_KEY")
ALGORITHM = os.environ.get("ALGORITHM")
ACCESS_TOKEN_EXPIRE_DAYS = int(os.environ.get("ACCESS_TOKEN_EXPIRE_DAYS")) # type: ignore
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def verify_password(password, hashed_password):
    return pwd_context.verify(password, hashed_password)


def hash_password(password):
    return pwd_context.hash(password)


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)  # type: ignore
    return encoded_jwt


def verify_access_token(token: str = "", payload: dict = {}):
    if token:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

    try:
        expire_date = datetime.fromtimestamp(payload.get("exp")).astimezone(
            tz=timezone.utc
        )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalide token"
        )

    if expire_date and expire_date < datetime.now(tz=timezone.utc):
        raise HTTPException(403, "Token has expired")


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    from .services import get_user

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])  # type: ignore
    except JWTError:
        raise credentials_exception

    verify_access_token(payload=payload)

    try:
        email = payload.get("email", None)
        user = get_user({"email": email})

        if not user:
            raise credentials_exception
    except Exception:
        raise credentials_exception

    return UserResponse(**user)


async def get_current_active_user(
    current_user: Annotated[UserResponse, Depends(get_current_user)],
):
    
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Account is inactive")

    return current_user
