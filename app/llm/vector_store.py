from sqlalchemy import select

from app.db.engine import async_session_maker
from app.db.tables import File, VectorStore

from . import client


async def get_vector_store() -> VectorStore:
    async with async_session_maker() as session:
        vector_stores = await session.execute(select(VectorStore))
        vector_store = vector_stores.scalars().first()
        if vector_store is None:
            result = client.vector_stores.create(name="chatbot_vector_store")
            vector_store = VectorStore(id=result.id)
            session.add(vector_store)
            await session.commit()
            await session.refresh(vector_store)

    return vector_store


async def create_file(file_path: str):
    vector_store = await get_vector_store()

    with open(file_path, "rb") as file_content:
        file = client.files.create(file=file_content, purpose="assistants")

    client.vector_stores.files.create(vector_store_id=vector_store.id, file_id=file.id)

    async with async_session_maker() as session:
        new_file = File(id=file.id, vector_store_id=vector_store.id)
        session.add(new_file)
        await session.commit()
        await session.refresh(new_file)


async def setup_vector_store():
    print("Setting up vector store")
    await get_vector_store()
