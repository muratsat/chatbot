from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel, Field

from app.config import env
from app.llm.assistant import generate_response
from app.telegram.messages import send_message

router = APIRouter(prefix="/telegram")


class From(BaseModel):
    id: int
    is_bot: bool | None = None
    first_name: str | None = None
    username: str | None = None
    language_code: str | None = None


class Chat(BaseModel):
    id: int
    first_name: str | None = None
    username: str | None = None
    type: str | None = None


class Message(BaseModel):
    message_id: int
    from_: From = Field(alias="from")
    chat: Chat
    date: int
    text: str


class TelegramWebhookPayload(BaseModel):
    update_id: int
    message: Message


@router.post("")
async def telegram_webhook(body: TelegramWebhookPayload, request: Request):
    """
    Handle incoming webhook requests from Telegram.
    Setup telegram webhook to point to this endpoint:

    https://api.telegram.org/bot{my_bot_token}/setWebhook?url={url_to_send_updates_to}&secret_token={webhook_token}

    my_bot_token = env.TG_BOT_API_TOKEN

    webhook_token = env.TG_WEBHOOK_TOKEN
    """

    secret_token = request.headers.get("X-Telegram-Bot-Api-Secret-Token")

    if secret_token != env.TG_WEBHOOK_TOKEN:
        raise HTTPException(
            status_code=403,
            detail="Invalid secret token",
        )

    response_message = await generate_response(
        user_id=str(body.message.from_.id),
        type="tg",
        message_id=f"{body.message.from_.id}-{body.message.message_id}",
        text=body.message.text,
    )

    await send_message(body.message.chat.id, response_message)
    return {"success": True}
