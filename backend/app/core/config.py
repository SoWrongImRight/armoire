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


settings = Settings()
