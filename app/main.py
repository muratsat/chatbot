import asyncio

from fastapi import FastAPI

from app.routers import telegram

app = FastAPI()

app.include_router(telegram.router)
