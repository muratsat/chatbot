import asyncio
import os

from app.llm import client
from app.llm.vector_store import get_vector_store


async def main():
    vector_store = await get_vector_store()

    previous_response_id = None

    while True:
        user_query = input(f"User: ")

        if user_query.lower() in ["q", "й", "quit"]:
            break

        response = client.responses.create(
            model="gpt-4o-mini",
            input=user_query,
            tools=[
                {
                    "type": "file_search",
                    "vector_store_ids": [vector_store.id],
                }
            ],
            previous_response_id=previous_response_id,
        )

        previous_response_id = response.id

        print(response.output_text)


if __name__ == "__main__":
    asyncio.run(main())
