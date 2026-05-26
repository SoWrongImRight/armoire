import os

from dotenv import load_dotenv

load_dotenv()


class Settings:
    # S3-compatible object storage (MinIO locally, AWS S3 in production).
    # S3_ENDPOINT_URL is reached by the backend (e.g. the in-cluster service);
    # S3_PUBLIC_URL is the address the browser uses to load images.
    S3_ENDPOINT_URL = os.getenv("S3_ENDPOINT_URL", "http://localhost:9000")
    S3_PUBLIC_URL = os.getenv("S3_PUBLIC_URL", S3_ENDPOINT_URL)
    S3_ACCESS_KEY = os.getenv("S3_ACCESS_KEY", "minioadmin")
    S3_SECRET_KEY = os.getenv("S3_SECRET_KEY", "minioadmin")
    S3_BUCKET = os.getenv("S3_BUCKET", "armoire")
    S3_REGION = os.getenv("S3_REGION", "us-east-1")

    # Auth / JWT
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-change-me")
    JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))

    # Weather (OpenWeather)
    OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY", "")
    WEATHER_DEFAULT_CITY = os.getenv("WEATHER_DEFAULT_CITY", "Orlando")

    # AI styling (Anthropic / Claude)
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
    ANTHROPIC_MODEL = os.getenv("ANTHROPIC_MODEL", "claude-opus-4-7")


settings = Settings()
