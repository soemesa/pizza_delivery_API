import uvicorn
from fastapi import FastAPI
from src.rotas.auth import router
from src.rotas.orders import order_router

app = FastAPI()


app.include_router(router)
app.include_router(order_router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", log_level="debug", port=8001, reload=True)
