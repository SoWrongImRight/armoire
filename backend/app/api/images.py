from fastapi import APIRouter, File, HTTPException, UploadFile

from app.services import storage_service

router = APIRouter(prefix="/images", tags=["images"])

ALLOWED_CONTENT_TYPES = {"image/jpeg", "image/png", "image/gif", "image/webp"}


@router.get("")
def list_images():
    return {"images": storage_service.list_images()}


@router.post("", status_code=201)
async def upload_image(file: UploadFile = File(...)):
    if file.content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type: {file.content_type or 'unknown'}",
        )
    key = storage_service.upload_fileobj(file.file, file.content_type, file.filename)
    return {"key": key, "url": storage_service.public_url(key)}
