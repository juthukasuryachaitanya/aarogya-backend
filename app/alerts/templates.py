# app/alerts/templates.py

def new_subscription(data: dict) -> str:
    return (
        "🆕 New Subscription\n"
        f"Name: {data['name']}\n"
        f"Plan: {data['plan']}\n"
        f"Community: {data['community']}\n"
        f"Phone: {data['phone']}"
    )


def subscription_paused(data: dict) -> str:
    return (
        "⏸️ Subscription Paused\n"
        f"Customer: {data['name']}\n"
        f"Community: {data['community']}"
    )


def subscription_resumed(data: dict) -> str:
    return (
        "▶️ Subscription Resumed\n"
        f"Customer: {data['name']}"
    )


def daily_summary(data: dict) -> str:
    return (
        "📦 Daily Delivery Summary\n"
        f"Date: {data['date']}\n"
        f"Active Subscriptions: {data['count']}"
    )


def expiry_reminder(data: dict) -> str:
    return (
        "⚠️ Subscription Expiring Soon\n"
        f"Customer: {data['name']}\n"
        f"Expiry Date: {data['expiry']}"
    )
