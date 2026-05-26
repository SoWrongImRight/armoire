import uuid

import boto3
from botocore.client import Config

from app.core.config import settings

_session = boto3.session.Session()


def get_s3_client():
    # Path-style addressing is required for MinIO and other non-AWS S3 endpoints.
    return _session.client(
        "s3",
        endpoint_url=settings.S3_ENDPOINT_URL,
        aws_access_key_id=settings.S3_ACCESS_KEY,
        aws_secret_access_key=settings.S3_SECRET_KEY,
        region_name=settings.S3_REGION,
        config=Config(signature_version="s3v4", s3={"addressing_style": "path"}),
    )


def ensure_bucket():
    client = get_s3_client()
    existing = [b["Name"] for b in client.list_buckets().get("Buckets", [])]
    if settings.S3_BUCKET not in existing:
        client.create_bucket(Bucket=settings.S3_BUCKET)


def public_url(key):
    return f"{settings.S3_PUBLIC_URL.rstrip('/')}/{settings.S3_BUCKET}/{key}"


def upload_fileobj(fileobj, content_type, original_name):
    ext = ""
    if original_name and "." in original_name:
        ext = "." + original_name.rsplit(".", 1)[1].lower()
    key = f"{uuid.uuid4().hex}{ext}"
    get_s3_client().upload_fileobj(
        fileobj,
        settings.S3_BUCKET,
        key,
        ExtraArgs={"ContentType": content_type or "application/octet-stream"},
    )
    return key


def list_images():
    resp = get_s3_client().list_objects_v2(Bucket=settings.S3_BUCKET)
    items = [
        {
            "key": obj["Key"],
            "url": public_url(obj["Key"]),
            "size": obj["Size"],
            "last_modified": obj["LastModified"].isoformat(),
        }
        for obj in resp.get("Contents", [])
    ]
    items.sort(key=lambda x: x["last_modified"], reverse=True)
    return items
