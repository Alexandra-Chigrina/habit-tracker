import requests
from config import settings


def send_telegram_message(chat_id, message):
    """Функция отправки уведомления в телеграмм."""
    params = {
        "text": message,
        "chat_id": chat_id
    }
    url = f"{settings.TELEGRAM_URL}{settings.TELEGRAM_TOKEN}/sendMessage"
    response = requests.get(url, params=params)

    if not response.ok:
        print("❌ Ошибка отправки в Telegram:", response.status_code, response.text)
    else:
        print(f"✅ Успешно отправлено сообщение: {message}")
