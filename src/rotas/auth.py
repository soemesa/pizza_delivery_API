from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette.responses import Response

from src.database import get_session
from src.schemas import UserSign, DefaultOut, Token, UserLogin
from src.security import get_current_active_user, oauth2_scheme
from src.service import Service
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

router = APIRouter(
    prefix='/auth',
    tags=['auth']
)


@router.get('/')
def hello():
    return "Welcome to Pizzary Delivery"


@router.get('/users/me')
def user(token: str = Depends(oauth2_scheme)):
    return "I am an User"


@router.post('/signup', response_model=DefaultOut, status_code=201)
def signup(user: UserSign, response: Response, session: Session = Depends(get_session)):
    service = Service()
    db_user = service.service_signup(response, user, session)
    return db_user


# @auth_router.post('/login', response_model=DefaultOut, status_code=200)
# def login(response: Response, user: UserLogin, session: Session = Depends(get_session)):
#     service = Service()
#     db_user = service.service_login(response, user, session)
#
#     return db_user


@router.post('/token', response_model=Token)
def login_token(form_data: OAuth2PasswordRequestForm = Depends(),
                session: Session = Depends(get_session)):
    service = Service()
    db_user = service.service_login_for_access_token(form_data, session)

    return db_user


# @auth_router.get('/users/me', response_model=UserSign)
# async def read_users_me(current_user: Annotated[UserSign, Depends(get_current_active_user)]):
#     return current_user

# @auth_router.get('users/me', dependencies=[Depends(check_token)])
# async def read_me(current_user: TokenData):
#     return current_user


