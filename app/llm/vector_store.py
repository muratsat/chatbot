from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.engine import async_session_maker
from app.db.tables import VectorStore

from . import client


def create_file(file_path: str):
    with open(file_path, "rb") as file_content:
        result = client.files.create(file=file_content, purpose="assistants")

    return result.id


async def setup_vector_store():
    print("Setting up vector store")
    async with async_session_maker() as session:
        vector_stores = await session.execute(select(VectorStore))

        vector_store = vector_stores.scalars().first()

        if vector_store is None:
            result = client.vector_stores.create(name="chatbot_vector_store")
            vector_store = VectorStore(id=result.id)

        session.add(vector_store)
        await session.commit()
        await session.refresh(vector_store)
