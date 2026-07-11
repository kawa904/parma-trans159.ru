from fastapi import APIRouter, Request, Form, HTTPException
from fastapi.responses import JSONResponse
from app.services.telegram import send_telegram_message
from app.database import save_order
import re

router = APIRouter(prefix="/api", tags=["form"])


@router.post("/order")
async def create_order(
        request: Request,
        name: str = Form(...),
        phone: str = Form(...),
        message: str = Form(...),
        consent: str = Form(...),
        consent_ads: str = Form(None)
):
    # 1. Валидация телефона
    if not re.match(r'^\+?[0-9]{10,15}$', phone):
        raise HTTPException(400, "Неверный формат телефона")

    # 2. Согласие обязательно!
    if consent != "on":
        raise HTTPException(400, "Необходимо согласие на обработку ПД")

    # 3. Сохраняем в базу с IP и User-Agent
    client_ip = request.client.host
    user_agent = request.headers.get("user-agent", "")

    order_data = {
        "name": name,
        "phone": phone,
        "message": message,
        "consent": True,
        "consent_ads": consent_ads == "on",
        "ip": client_ip,
        "user_agent": user_agent
    }
    await save_order(order_data)

    # 4. Отправка в Telegram
    await send_telegram_message(name, phone, message)

    return JSONResponse({"status": "ok", "message": "Заявка принята!"})