# from fastapi import Depends, HTTPException
# from fastapi_jwt_auth import AuthJWT
# from fastapi_jwt_auth.exceptions import AuthJWTException
# from sqlalchemy.exc import IntegrityError
#
# from src.schemas import DefaultOut
from werkzeug.security import generate_password_hash

from src.models import User
from src.schemas import DefaultOut


class Service:
    @staticmethod
    def service_signup(response, user, session):
        try:
            db_email = session.query(User).filter(User.email == user.email).first()
            if db_email is not None:
                response.status_code = 400
                return DefaultOut(status='error', message='User with the email already exists')

            db_username = session.query(User).filter(User.username == user.username).first()
            if db_username is not None:
                response.status_code = 400
                return DefaultOut(status='error', message='User with the username already exists')

            new_user = User(
                username=user.username,
                email=user.email,
                password=generate_password_hash(user.password),
                is_active=user.is_active,
                is_staff=user.is_staff
            )

            session.add(new_user)
            session.commit()
            session.refresh(new_user)
        except Exception as err:
            return DefaultOut(status='error', message=f'{err}')

        return DefaultOut(status='signed', message='User successfully signed')



















#     @staticmethod
#     def verificar_authenticacao_jwt(response, Authorize: AuthJWT = Depends()):
#         try:
#             Authorize.jwt_required()
#         except AuthJWTException as e:
#             raise HTTPException(status_code=401, detail=str(e))
#
#         return DefaultOut(status='authorized', message='Token valid')

        # if Authorize.payload['token'] == 'b4bb9013c1c03b29b9311ec0df07f3b0d8fd13edd02d5c45b2fa7b86341fa405':
        #     return {"message": "Hello World"}
        # else:
        #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
        #                         detail="Invalid Token"
        #                         )
        #
