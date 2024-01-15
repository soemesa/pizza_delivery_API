# from email_validator import validate_email
from pydantic import BaseModel

from src.models import User


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class UserModel(BaseModel):
    username: str
    email: str | None = None
    disabled: bool | None = None


class UserLogin(BaseModel):
    username: str
    password: str


class UserSign(BaseModel):
    id: int | None = None
    username: str
    email: str
    password: str
    is_staff: bool | None = None
    is_active: bool | None = None

    class Config:
        from_attributes = True
        json_schema_extra = {
            'example': {
                "username": "johndoe",
                "email": "johndoe@gmail.com",
                "password": "password",
                "is_staff": False,
                "is_active": True
            }
        }


class DefaultOut(BaseModel):
    status: str
    message: str


# class OrderModel(BaseModel):
#     id: int | None = None
#     quantity: int
#     order_status: str = "PENDING"
#     pizza_size: str = "SMALL"
#     user_id: int | None = None
#
#     class Config:
#         from_attributes = True
#         json_schema_extra = {
#             "example": {
#                 "quantity": 2,
#                 "pizza_size": "LARGE"
#             }
#         }

# class OrderStatusModel(BaseModel):
#     order_status: str = "PENDING"
#
#     class Config:
#         from_attributes = True
#         json_schema_extra = {
#             "example": {
#                 "order_status": "PENDING"
#             }
#         }
