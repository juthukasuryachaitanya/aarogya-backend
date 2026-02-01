import os

class Settings:
    APP_NAME: str = os.getenv("APP_NAME", "Aarogya Harvest")
    ENV: str = os.getenv("ENV", "development")

    # ======================
    # JWT CONFIG
    # ======================
    JWT_SECRET: str = os.getenv("JWT_SECRET")
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
    JWT_EXPIRE_MINUTES: int = int(os.getenv("JWT_EXPIRE_MINUTES", "60"))

    # ======================
    # DATABASE CONFIG
    # ======================
    DATABASE_URL: str = os.getenv("DATABASE_URL")

    # ======================
    # CORS
    # ======================
    ALLOWED_ORIGINS = os.getenv(
        "ALLOWED_ORIGINS",
        "http://localhost:5173"
    ).split(",")

    # ======================
    # VALIDATION
    # ======================
    def validate(self):
        if not self.JWT_SECRET:
            raise RuntimeError("❌ JWT_SECRET is not set")

        if not self.DATABASE_URL:
            raise RuntimeError("❌ DATABASE_URL is not set")

settings = Settings()
settings.validate()
