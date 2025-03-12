import asyncio

from fastapi import FastAPI

from app.db.engine import create_db_and_tables
from app.llm.vector_store import setup_vector_store
from app.routers import telegram


async def on_startup():
    await create_db_and_tables()
    await setup_vector_store()


app = FastAPI()
app.add_event_handler("startup", on_startup)
app.include_router(telegram.router)
