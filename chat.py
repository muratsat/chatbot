import asyncio
import os
import uuid

from app.llm import client
from app.llm.assistant import generate_response
from app.llm.vector_store import get_vector_store


async def main():
    vector_store = await get_vector_store()

    user_id = "cli"

    previous_response_id = None

    while True:
        user_query = input(f"User: ")

        if user_query.lower() in ["q", "й", "quit"]:
            break

        message_id = str(uuid.uuid4())

        response = await generate_response(user_id, "cli", message_id, user_query)
        print("Assistant:", response)


if __name__ == "__main__":
    asyncio.run(main())
