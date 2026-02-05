import os


class settings:
    # ======================
    # APP CONFIG
    # ======================
    APP_NAME: str = os.getenv("APP_NAME", "Aarogya Harvest API")
    ENV: str = os.getenv("ENV", "development")

    # ======================
    # JWT CONFIG
    # ======================
    JWT_SECRET: str | None = os.getenv("JWT_SECRET")
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
    JWT_EXPIRE_MINUTES: int = int(
        os.getenv("JWT_EXPIRE_MINUTES", "60")
    )

    # ======================
    # DATABASE CONFIG
    # ======================
    DATABASE_URL: str | None = os.getenv("DATABASE_URL")

    # ======================
    # CORS CONFIG
    # ======================
    ALLOWED_ORIGINS: list[str] = os.getenv(
        "ALLOWED_ORIGINS",
        "http://localhost:5173"
    ).split(",")

    # ======================
    # VALIDATION (FAIL FAST)
    # ======================
    def validate(self) -> None:
        if not self.JWT_SECRET:
            raise RuntimeError("❌ JWT_SECRET is not set")

        if not self.DATABASE_URL:
            raise RuntimeError("❌ DATABASE_URL is not set")


# Singleton settings instance
settings = settings()
settings.validate()
