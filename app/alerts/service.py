
from app.alerts import templates
from app.core.logger import logger


def send_admin_alert(alert_type: str, data: dict):
    """
    Central admin alert dispatcher (INTERNAL ONLY)

    Alerts handled:
    1. New subscription
    2. Pause
    3. Resume
    4. Daily summary
    5. Expiry reminder

    NOTE:
    - WhatsApp removed
    - Alerts are logged only
    """

    try:
        # -------------------------
        # MESSAGE BUILDING
        # -------------------------
        if alert_type == "NEW_SUBSCRIPTION":
            message = templates.new_subscription(data)

        elif alert_type == "SUBSCRIPTION_PAUSED":
            message = templates.subscription_paused(data)

        elif alert_type == "SUBSCRIPTION_RESUMED":
            message = templates.subscription_resumed(data)

        elif alert_type == "DAILY_SUMMARY":
            message = templates.daily_summary(data)

        elif alert_type == "EXPIRY_REMINDER":
            message = templates.expiry_reminder(data)

        else:
            logger.warning(f"[ALERT] Unknown alert type: {alert_type}")
            return

        # -------------------------
        # LOG ONLY (SAFE MODE)
        # -------------------------
        logger.info(
            f"""
================ ADMIN ALERT =================
TYPE: {alert_type}
MESSAGE:
{message}
=============================================
"""
        )

    except Exception as e:
        # Never break business flow due to alerts
        logger.error(
            f"[ALERT FAILED] Type={alert_type} Error={str(e)}",
            exc_info=True
        )
