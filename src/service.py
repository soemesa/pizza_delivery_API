from typing import Annotated

from fastapi import Depends
from fastapi.exceptions import ResponseValidationError, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from starlette.responses import Response

from src.database import get_session
from src.models import User
from src.schemas import DefaultOut, Token
from src.security import get_password_hash, verify_password, create_access_token


class Service:
    @staticmethod
    def service_signup(response, user, session: Session = Depends(get_session)):
        try:
            user_model = session.query(User).filter(User.username == user.username).first()
            if user_model:
                response.status_code = 400
                return DefaultOut(status='error', message='Username already exists')

            hashed_password = get_password_hash(user.password)

            new_user = User(
                username=user.username,
                email=user.email,
                password=hashed_password,
                is_active=user.is_active,
                is_staff=user.is_staff
            )

            session.add(new_user)
            session.commit()
            session.refresh(new_user)
        except Exception as err:
            return DefaultOut(status='error', message=f'{err}')

        return DefaultOut(status='signed', message='User successfully signed')

    @staticmethod
    def service_login(response, user, session: Session = Depends(get_session)):

        if not user.username or not user.password:
            response.status_code = 400
            return DefaultOut(status='invalid', message='Username and password are required')

        try:
            db_user = session.query(User).filter(User.username == user.username).first()
        except SQLAlchemyError:
            response.status_code = 500
            return DefaultOut(status='error', message='An error occurred during login')

        if not db_user or not user.password:
            response.status_code = 400
            return DefaultOut(status='invalid', message='Username or Password not found')

        if not verify_password(user.password, db_user.password):
            response.status_code = 400
            return DefaultOut(status='invalid', message='Invalid Username or Password')

        return DefaultOut(status='loged', message="User successfully logged in")

    @staticmethod
    def service_login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                                       session: Session = Depends(get_session)):

        db_user = session.query(User).filter(
            User.username == form_data.username,
        ).scalar()

        if not db_user:
            raise HTTPException(status_code=400, detail='Invalid Username')

        verify = verify_password(form_data.password, db_user.password)

        if not verify:
            raise HTTPException(status_code=400, detail='Invalid Password')

        access_token = create_access_token(data={'sub': db_user.username})

        return Token(access_token=access_token, token_type='bearer')



