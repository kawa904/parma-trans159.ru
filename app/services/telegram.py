import aiohttp
from app.config import config


async def send_telegram_message(name: str, phone: str, message: str):
    """Отправка заявки в Telegram"""
    from datetime import datetime

    text = (
        f"🚛 **НОВАЯ ЗАЯВКА НА ПЕРЕВОЗКУ**\n\n"
        f"👤 Имя: {name}\n"
        f"📞 Телефон: {phone}\n"
        f"📝 Детали: {message}\n"
        f"🕐 Время: {datetime.now().strftime('%d.%m.%Y %H:%M')}"
    )

    url = f"https://api.telegram.org/bot{config.TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": config.TELEGRAM_CHAT_ID,
        "text": text,
        "parse_mode": "Markdown"
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=payload) as resp:
            return await resp.json()