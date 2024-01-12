from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette.responses import Response

from src.database import get_session
from src.schemas import UserSign, DefaultOut, Token, UserLogin
from src.service import Service
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

auth_router = APIRouter(
    prefix='/auth',
    tags=['auth']
)


@auth_router.get('/')
def hello():
    return {'message': 'Hello World'}


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@auth_router.get("/users/")
async def read_users(token: Annotated[str, Depends(oauth2_scheme)]):
    return {"token": token}


@auth_router.post('/signup', response_model=DefaultOut, status_code=201)
async def signup(user: UserSign, response: Response, session: Session = Depends(get_session)):
    service = Service()
    db_user = service.service_signup(response, user, session)

    return db_user


@auth_router.post('/login', response_model=DefaultOut, status_code=200)
def login(response: Response, user: UserLogin, session: Session = Depends(get_session)):
    service = Service()
    db_user = service.service_login(response, user, session)

    return db_user


@auth_router.post('/token', response_model=Token)
def login_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                session: Session = Depends(get_session)):
    service = Service()
    db_user = service.service_login_for_access_token(form_data, session)

    return db_user


# @auth_router.get('users/me', response_model=UserSign)
# async def read_me(current_user: UserSign = Depends(get_current_active_user)):
#     return current_user

# @auth_router.get('users/me', dependencies=[Depends(check_token)])
# async def read_me(current_user: TokenData):
#     return current_user


