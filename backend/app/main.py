from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from app.api import images, items
from app.db import models  # noqa: F401  (register models on Base)
from app.db.database import Base, engine
from app.db.session import get_db
from app.services import storage_service

app = FastAPI()

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)
    # The compose init job also creates the bucket; this is a best-effort
    # safety net so the app still works when run outside compose.
    try:
        storage_service.ensure_bucket()
    except Exception as exc:  # noqa: BLE001
        print(f"ensure_bucket warning: {exc}")


app.include_router(images.router)
app.include_router(items.router)


@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI application!"}


@app.get("/healthcheck")
def health_check(db: Session = Depends(get_db)):
    return {"status": "ok"}
