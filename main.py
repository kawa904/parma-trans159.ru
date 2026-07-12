from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
import requests
import os

app = FastAPI()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# ===== ГЛАВНАЯ =====
@app.get("/", response_class=HTMLResponse)
async def index():
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>ПАРМА ТРАНС</title>
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body { font-family: Arial, sans-serif; background: #0b1a2e; display: flex; justify-content: center; align-items: center; min-height: 100vh; padding: 20px; }
            .card { background: linear-gradient(145deg, #102b3f, #1a3a4f); padding: 40px; border-radius: 32px; max-width: 440px; width: 100%; box-shadow: 0 30px 60px rgba(0,0,0,0.8); }
            h1 { color: #f5c842; text-align: center; font-size: 28px; margin-bottom: 4px; }
            .sub { color: #b6d0e0; text-align: center; font-size: 14px; margin-bottom: 24px; }
            input, textarea { width: 100%; padding: 14px; border-radius: 14px; border: 1.5px solid rgba(255,255,255,0.08); margin-bottom: 14px; font-size: 16px; background: rgba(255,255,255,0.06); color: white; box-sizing: border-box; }
            input:focus, textarea:focus { border-color: #f5c842; outline: none; }
            textarea { min-height: 90px; resize: vertical; }
            .checkbox-group { display: flex; align-items: flex-start; gap: 12px; margin: 12px 0; font-size: 14px; color: #b6d0e0; }
            .checkbox-group input[type="checkbox"] { width: 20px; height: 20px; flex-shrink: 0; margin-top: 2px; accent-color: #f5c842; cursor: pointer; }
            .checkbox-group label { cursor: pointer; line-height: 1.4; }
            .checkbox-group a { color: #f5c842; text-decoration: none; border-bottom: 1px dashed rgba(245,200,66,0.3); }
            button { width: 100%; padding: 16px; border: none; border-radius: 60px; background: linear-gradient(135deg, #f5c842, #e8a820); font-weight: 800; font-size: 18px; color: #0b1a2e; cursor: pointer; transition: 0.3s; margin-top: 6px; }
            button:hover { transform: translateY(-2px); }
            #status { margin-top: 16px; text-align: center; font-weight: 600; min-height: 24px; }
            .success { color: #81c784; }
            .error { color: #ef9a9a; }
            .footer { margin-top: 20px; padding-top: 16px; border-top: 1px solid rgba(255,255,255,0.06); text-align: center; font-size: 12px; color: #9bb8d0; }
            .footer a { color: #f5c842; text-decoration: none; }
            .required { color: #f5c842; }
        </style>
    </head>
    <body>
        <div class="card">
            <h1>🚛 ПАРМА ТРАНС</h1>
            <p class="sub">Перевозки по Пермскому краю</p>

            <form id="form">
                <input type="text" id="name" placeholder="Ваше имя" required>
                <input type="tel" id="phone" placeholder="Телефон" required>
                <textarea id="message" placeholder="Описание груза (город, вес)"></textarea>

                <div class="checkbox-group">
                    <input type="checkbox" id="consent" required>
                    <label for="consent">
                        Согласие на обработку данных по <a href="/consent" target="_blank">ФЗ-152</a>
                        <span class="required">*</span>
                    </label>
                </div>

                <button type="submit">ОТПРАВИТЬ</button>
                <div id="status"></div>
            </form>

            <div class="footer">
                <a href="/policy">Политика конфиденциальности</a>
            </div>
        </div>

        <script>
            document.getElementById('form').onsubmit = async (e) => {
                e.preventDefault();
                const status = document.getElementById('status');
                if (!document.getElementById('consent').checked) {
                    status.className = 'error';
                    status.textContent = '❌ Дайте согласие на обработку данных';
                    return;
                }
                status.className = '';
                status.textContent = '⏳ Отправка...';
                try {
                    const res = await fetch('/send', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({
                            name: document.getElementById('name').value,
                            phone: document.getElementById('phone').value,
                            message: document.getElementById('message').value
                        })
                    });
                    const data = await res.json();
                    if (data.ok) {
                        status.className = 'success';
                        status.textContent = '✅ Заявка отправлена!';
                        document.getElementById('form').reset();
                    } else {
                        status.className = 'error';
                        status.textContent = '❌ Ошибка, попробуйте позже';
                    }
                } catch {
                    status.className = 'error';
                    status.textContent = '❌ Ошибка соединения';
                }
            };
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html)

# ===== ОТПРАВКА =====
@app.post("/send")
async def send(data: dict):
    text = f"📦 НОВАЯ ЗАЯВКА\n\n👤 {data.get('name')}\n📞 {data.get('phone')}\n📝 {data.get('message')}"
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    try:
        r = requests.post(url, json={"chat_id": TELEGRAM_CHAT_ID, "text": text})
        return {"ok": r.status_code == 200}
    except:
        return {"ok": False}

# ===== СОГЛАСИЕ =====
@app.get("/consent", response_class=HTMLResponse)
async def consent():
    return HTMLResponse("""
    <!DOCTYPE html>
    <html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>Согласие</title>
    <style>body{font-family:Arial;background:#0b1a2e;padding:40px 20px;display:flex;justify-content:center;}.doc{background:#1a3a4f;padding:40px;border-radius:32px;max-width:800px;color:#e0e8f0;box-shadow:0 30px 60px rgba(0,0,0,0.7);}h1{color:#f5c842;border-bottom:2px solid #f5c842;padding-bottom:12px;}h2{color:#f5c842;margin-top:24px;}p{line-height:1.6;}ul{margin:8px 0 12px 24px;}.back{color:#f5c842;text-decoration:none;border-bottom:1px dashed rgba(245,200,66,0.3);}</style>
    </head><body><div class="doc"><h1>СОГЛАСИЕ НА ОБРАБОТКУ ПЕРСОНАЛЬНЫХ ДАННЫХ</h1>
    <p><strong>Владелец:</strong> Казанцев Максим (ИНН 595152008597)<br><strong>Адрес:</strong> г. Пермь</p>
    <p>Я даю согласие на обработку моих персональных данных (ФИО, телефон, данные о грузе) для связи по заявке.</p>
    <h2>Цели</h2><p>Обработка заявок, заключение договоров перевозки, информирование.</p>
    <h2>Срок хранения</h2><p>3 года.</p>
    <h2>Отзыв согласия</h2><p>Письмо на email: <strong>support@parmatrans159.ru</strong></p>
    <p style="margin-top:30px;"><em>Дата: 12.07.2026</em></p>
    <a href="/" class="back">← На главную</a>
    </div></body></html>
    """)

# ===== ПОЛИТИКА =====
@app.get("/policy", response_class=HTMLResponse)
async def policy():
    return HTMLResponse("""
    <!DOCTYPE html>
    <html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>Политика</title>
    <style>body{font-family:Arial;background:#0b1a2e;padding:40px 20px;display:flex;justify-content:center;}.doc{background:#1a3a4f;padding:40px;border-radius:32px;max-width:800px;color:#e0e8f0;box-shadow:0 30px 60px rgba(0,0,0,0.7);}h1{color:#f5c842;border-bottom:2px solid #f5c842;padding-bottom:12px;}h2{color:#f5c842;margin-top:24px;}p{line-height:1.6;}ul{margin:8px 0 12px 24px;}.back{color:#f5c842;text-decoration:none;border-bottom:1px dashed rgba(245,200,66,0.3);}</style>
    </head><body><div class="doc"><h1>ПОЛИТИКА КОНФИДЕНЦИАЛЬНОСТИ</h1>
    <p><strong>Владелец:</strong> Казанцев Максим (ИНН 595152008597)<br><strong>Email:</strong> support@parmatrans159.ru</p>
    <h2>1. Общие положения</h2><p>Порядок обработки персональных данных.</p>
    <h2>2. Какие данные собираются</h2><ul><li>ФИО</li><li>Телефон</li><li>Данные о грузе</li><li>IP-адрес (техническая безопасность)</li></ul>
    <h2>3. Цели</h2><ul><li>Обработка заявок</li><li>Заключение договоров</li><li>Информирование</li></ul>
    <h2>4. Передача третьим лицам</h2><p>Не передаются, кроме случаев, предусмотренных законом.</p>
    <h2>5. Меры защиты</h2><ul><li>HTTPS</li><li>Защищённый сервер</li></ul>
    <h2>6. Права</h2><p>Отзыв согласия, запрос копии данных, удаление.</p>
    <p style="margin-top:30px;"><em>Дата: 12.07.2026</em></p>
    <a href="/" class="back">← На главную</a>
    </div></body></html>
    """)
