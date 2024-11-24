from fastapi import FastAPI
from src.routes import router

# Создание FastAPI приложения
app = FastAPI()

app.include_router(router)