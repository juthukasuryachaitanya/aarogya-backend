import requests
from app.core.config import settings

WHATSAPP_URL = (
    f"https://graph.facebook.com/v18.0/"
    f"{settings.WHATSAPP_PHONE_ID}/messages"
)

def send_whatsapp_message(text: str):
    payload = {
        "messaging_product": "whatsapp",
        "to": settings.ADMIN_PHONE,
        "type": "text",
        "text": {"body": text},
    }

    headers = {
        "Authorization": f"Bearer {settings.WHATSAPP_TOKEN}",
        "Content-Type": "application/json",
    }

    response = requests.post(
        WHATSAPP_URL,
        json=payload,
        headers=headers,
        timeout=10
    )

    if response.status_code >= 400:
        raise Exception(response.text)
