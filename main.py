from fastapi import FastAPI

from src.auth_routes import auth_router
from src.order_routes import order_router

app = FastAPI()

app.include_router(auth_router)
app.include_router(order_router)
