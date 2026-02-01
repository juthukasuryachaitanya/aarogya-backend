from app.core.logger import logger

def send_admin_alert(alert_type: str, payload: dict):
    """
    Central alert dispatcher.
    Later this will connect to SMS / WhatsApp.
    """

    logger.info(
        f"[ADMIN ALERT] {alert_type} | {payload}"
    )

    # Future:
    # send_sms()
    # send_whatsapp()

