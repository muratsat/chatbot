from typing import Literal

from sqlalchemy import asc, select

from app.db.actions import create_message, create_user
from app.db.engine import async_session_maker
from app.db.tables import Message, User
from app.llm.vector_store import get_vector_store

from . import client, prompt


async def generate_response(
    user_id: str,
    type: Literal["whatsapp", "telegram", "cli"],
    message_id: str,
    text: str,
):
    vector_store = await get_vector_store()
    user_id = type + "-" + user_id

    async with async_session_maker() as session:
        user = await session.execute(select(User).where(User.id == user_id))
        user = user.scalars().first()

        if user is None:
            user = User(id=user_id, type=type)
            await create_user(session, user)

        msg_id = type + "-" + message_id
        user_message = Message(id=msg_id, user_id=user_id, content=text, role="user")
        await create_message(session, user_message)

        messages = await session.execute(
            select(Message)
            .where(
                Message.user_id == user_id,
            )
            .order_by(asc(Message.date))
        )
        messages = messages.scalars().all()

        response = client.responses.create(
            model="gpt-4o-mini",
            input=[
                {"role": "system", "content": prompt},
            ]
            + [{"role": msg.role, "content": msg.content} for msg in messages],
            tools=[
                {
                    "type": "file_search",
                    "vector_store_ids": [vector_store.id],
                }
            ],
        )

        ai_msg_id = type + "-" + response.id
        ai_message = Message(
            id=ai_msg_id,
            user_id=user_id,
            content=response.output_text,
            response_id=response.id,
            role="assistant",
        )
        await create_message(session, ai_message)

    return response.output_text
