from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# ==============================
# CORE CONFIG
# ==============================
from app.core.config import settings

# ==============================
# RATE LIMITING (ANTI-SCRAPING)
# ==============================
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from app.core.rate_limit import limiter

# ==============================
# ROUTERS
# ==============================
from app.auth.router import router as auth_router
from app.users.router import router as users_router
from app.subscriptions.router import router as subscriptions_router

from app.admin.router import router as admin_auth_router
from app.admin.customers import router as admin_customers_router
from app.admin.deliveries import router as admin_deliveries_router
from app.admin.finance import router as finance_router
from app.expenses.router import router as expenses_router

# ==============================
# SCHEDULER + JOBS (STEP 7)
# ==============================
from app.core.scheduler import scheduler
from app.jobs.delivery_summary import daily_delivery_summary
from app.jobs.expiry_reminders import subscription_expiry_reminders
from apscheduler.triggers.cron import CronTrigger

# ==============================
# APP INITIALIZATION
# ==============================
app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0",
)

# ==============================
# RATE LIMITER SETUP
# ==============================
app.state.limiter = limiter
app.add_exception_handler(
    RateLimitExceeded,
    _rate_limit_exceeded_handler
)

# ==============================
# CORS (LOCKED TO FRONTEND)
# ==============================
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==============================
# ROUTER REGISTRATION
# ==============================
app.include_router(auth_router)
app.include_router(users_router)
app.include_router(subscriptions_router)

app.include_router(admin_auth_router)
app.include_router(admin_customers_router)
app.include_router(admin_deliveries_router)
app.include_router(expenses_router)
app.include_router(finance_router)

# ==============================
# STARTUP / SHUTDOWN EVENTS
# ==============================
@app.on_event("startup")
def startup_event():
    """
    Register background jobs & start scheduler
    """

    # Daily delivery summary — 5:30 AM IST
    scheduler.add_job(
        daily_delivery_summary,
        CronTrigger(hour=5, minute=30),
        id="daily_delivery_summary",
        replace_existing=True,
    )

    # Subscription expiry reminders — 9:00 AM IST
    scheduler.add_job(
        subscription_expiry_reminders,
        CronTrigger(hour=9, minute=0),
        id="subscription_expiry_reminders",
        replace_existing=True,
    )

    if not scheduler.running:
        scheduler.start()


@app.on_event("shutdown")
def shutdown_event():
    scheduler.shutdown(wait=False)

# ==============================
# HEALTH CHECK
# ==============================
@app.get("/health", tags=["Health"])
def health_check():
    return {
        "status": "ok",
        "app": settings.APP_NAME,
        "env": settings.ENV,
    }
