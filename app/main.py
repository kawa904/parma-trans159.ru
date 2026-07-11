from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.middleware import SlowAPIMiddleware
from app.config import config
from app.database import init_db
from app.routers import form
import uvicorn

# Инициализация
app = FastAPI(title="Грузоперевозки 159")

# HTTPS-редирект ОТКЛЮЧЕН для локальной разработки
# app.add_middleware(HTTPSRedirectMiddleware)

# Защита от флуда (5 заявок в минуту с одного IP)
limiter = Limiter(key_func=get_remote_address, default_limits=["5/minute"])
app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)

# Подключаем статику и шаблоны
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

# Подключаем роутер форм
app.include_router(form.router)

# Событие запуска - создание базы данных
@app.on_event("startup")
async def on_startup():
    await init_db()

# ГЛАВНАЯ СТРАНИЦА
@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {
        "request": request,
        "site_name": config.SITE_NAME,
        "owner_name": config.OWNER_NAME,
        "owner_inn": config.OWNER_INN,
        "owner_address": config.OWNER_ADDRESS,
        "contact_phone": config.CONTACT_PHONE,
        "contact_email": config.CONTACT_EMAIL
    })

# СТРАНИЦА СОГЛАСИЯ (ФЗ-152)
@app.get("/consent")
async def consent_page(request: Request):
    return templates.TemplateResponse("consent.html", {
        "request": request,
        "owner_name": config.OWNER_NAME,
        "owner_inn": config.OWNER_INN,
        "owner_address": config.OWNER_ADDRESS,
        "site_name": config.SITE_NAME,
        "contact_email": config.CONTACT_EMAIL
    })

# СТРАНИЦА ПОЛИТИКИ КОНФИДЕНЦИАЛЬНОСТИ
@app.get("/policy")
async def policy_page(request: Request):
    return templates.TemplateResponse("policy.html", {
        "request": request,
        "owner_name": config.OWNER_NAME,
        "owner_inn": config.OWNER_INN,
        "site_name": config.SITE_NAME,
        "contact_email": config.CONTACT_EMAIL
    })

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)