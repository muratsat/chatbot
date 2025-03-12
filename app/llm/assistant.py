from typing import Literal

from sqlalchemy import and_, desc, select

from app.db.engine import async_session_maker
from app.db.tables import Message, User
from app.llm.vector_store import get_vector_store

from . import client


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
            session.add(user)
            await session.commit()
            await session.refresh(user)

        msg_id = type + "-" + message_id
        user_message = Message(id=msg_id, user_id=user_id, content=text)
        session.add(user_message)
        await session.commit()
        await session.refresh(user_message)

        last_response = await session.execute(
            select(Message)
            .where(and_(Message.user_id == user_id, Message.response_id.is_not(None)))
            .order_by(desc(Message.date))
        )
        last_response = last_response.scalars().first()

        prev_resp_id = last_response.response_id if last_response else None

        response = client.responses.create(
            model="gpt-4o-mini",
            input=text,
            tools=[
                {
                    "type": "file_search",
                    "vector_store_ids": [vector_store.id],
                }
            ],
            previous_response_id=prev_resp_id,
        )

        ai_msg_id = type + "-" + response.id
        ai_message = Message(
            id=ai_msg_id,
            user_id=user_id,
            content=response.output_text,
            response_id=response.id,
        )
        session.add(ai_message)
        await session.commit()
        await session.refresh(ai_message)

    return response.output_text
