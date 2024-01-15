from datetime import datetime, timedelta, timezone

from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.context import CryptContext
from starlette import status

from typing import Annotated

from src.models import User
from src.schemas import TokenData
from src.settings import Settings

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='auth/token')

settings = Settings()


def get_password_hash(password: str):
    out = pwd_context.hash(password)
    return out


def verify_password(plain_password: str, hashed_password: str):
    out = pwd_context.verify(plain_password, hashed_password)
    return out


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    user = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=settings.ALGORITHM)
        username: str = payload.get('sub')
        if username is None:
            raise user
        token_data = TokenData(username=username)
    except JWTError:
        raise user
    return token_data


async def get_current_active_user(current_user: Annotated[User, Depends(get_current_user)]):
    if current_user.is_active:
        raise HTTPException(status_code=400, detail='Inactive user')
    return current_user



