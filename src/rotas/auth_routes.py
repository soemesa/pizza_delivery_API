from typing import Union

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status
from starlette.responses import Response
from werkzeug.security import generate_password_hash

from src.database import get_session
from src.models import User
from src.schemas import SignUpModel, DefaultOut
from src.service import Service

# from fastapi_jwt_auth import AuthJWT
#
# from src.schemas import DefaultOut
# from src.service import Service

auth_router = APIRouter(
    prefix='/auth',
    tags=['auth']
)


@auth_router.get('/')
def hello():
    return {'message': 'Hello World'}


# @auth_router.get('/', response_model=DefaultOut, status_code=200)
# async def hello(Authorize: AuthJWT = Depends()) -> dict:
#     service = Service()
#     autorizacao = service.verificar_authenticacao_jwt(Authorize)
#
#     return autorizacao


@auth_router.post('/signup', response_model=SignUpModel | DefaultOut, status_code=201)
async def signup(user: SignUpModel, response: Response, session: Session = Depends(get_session)):
    service = Service()
    db_user = service.service_signup(response, user, session)

    return db_user


