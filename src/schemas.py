from pydantic import BaseModel
from typing import Optional


class SignUpModel(BaseModel):
    id: int | None = None
    username: str
    email: str
    password: str
    is_staff: bool | None = None
    is_active: bool | None = None

    class Config:
        orm_mode = True
        schema_extra = {
            'example': {
                "username": "johndoe",
                "email": "johndoe@gmail.com",
                "password": "password",
                "is_staff": False,
                "is_active": True
            }
        }


class Settings(BaseModel):
    authjwt_secret_key: str = 'b4bb9013c1c03b29b9311ec0df07f3b0d8fd13edd02d5c45b2fa7b86341fa405'


class LoginModel(BaseModel):
    username: str
    password: str


class OrderModel(BaseModel):
    id: int | None = None
    quantity: int
    order_status: str = "PENDING"
    pizza_size: str = "SMALL"
    user_id: int | None = None

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "quantity": 2,
                "pizza_size": "LARGE"
            }
        }


class OrderStatusModel(BaseModel):
    order_status: str = "PENDING"

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "order_status": "PENDING"
            }
        }
