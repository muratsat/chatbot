from fastapi import APIRouter, HTTPException, Request
from pydantic import ValidationError

from app.config import env
from app.llm import prompt
from app.llm.assistant import generate_response
from app.telegram.messages import send_message
from app.telegram.schemas import TelegramWebhookPayload

telegram_router = APIRouter(prefix="/telegram")


@telegram_router.post("")
async def telegram_webhook(request: Request):
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

    try:
        req_body = await request.json()
        body = TelegramWebhookPayload.model_validate(req_body)
        text = body.message.text
        if text.strip() == "/start":
            await send_message(body.message.chat.id, "Напишите любое сообщение")
            return {"success": True}

        print(f"Received messages from {body.message.chat.username}: {text}")
        response_message = await generate_response(
            user_id=str(body.message.from_.id),
            type="tg",
            message_id=f"{body.message.from_.id}-{body.message.message_id}",
            text=text,
        )
        await send_message(body.message.chat.id, response_message)

    except ValidationError:
        pass

    return {"success": True}
