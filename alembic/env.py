from logging.config import fileConfig
import os

from sqlalchemy import engine_from_config, pool
from alembic import context

# -------------------------
# Alembic Config
# -------------------------
config = context.config

# -------------------------
# Logging
# -------------------------
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# -------------------------
# Import Base + Models
# -------------------------
from app.core.database import Base
from app.subscriptions.models import Subscription
from app.expenses.models import Expense

target_metadata = Base.metadata

# -------------------------
# DATABASE URL (ENV FIRST)
# -------------------------
def get_database_url():
    return os.getenv("DATABASE_URL") or config.get_main_option(
        "sqlalchemy.url"
    )

# -------------------------
# OFFLINE MIGRATIONS
# -------------------------
def run_migrations_offline() -> None:
    """Run migrations without DB connection"""
    url = get_database_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        compare_type=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

# -------------------------
# ONLINE MIGRATIONS
# -------------------------
def run_migrations_online() -> None:
    """Run migrations with DB connection"""
    connectable = engine_from_config(
        {
            "sqlalchemy.url": get_database_url()
        },
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,   # 🔥 VERY IMPORTANT
            compare_server_default=True,
        )

        with context.begin_transaction():
            context.run_migrations()

# -------------------------
# MODE SWITCH
# -------------------------
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
