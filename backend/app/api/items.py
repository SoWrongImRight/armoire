from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.crud import item as crud
from app.db.models import Item
from app.db.session import get_db
from app.schemas.item import ItemCreate, ItemRead, ItemUpdate
from app.services import storage_service

router = APIRouter(prefix="/items", tags=["items"])


def serialize(item: Item) -> ItemRead:
    read = ItemRead.model_validate(item)
    if item.image_key:
        read.image_url = storage_service.public_url(item.image_key)
    return read


@router.get("/summary")
def summary(db: Session = Depends(get_db)):
    return crud.composition_summary(db)


@router.get("", response_model=list[ItemRead])
def list_items(
    category: Optional[str] = None,
    brand: Optional[str] = None,
    season: Optional[str] = None,
    db: Session = Depends(get_db),
):
    return [serialize(i) for i in crud.list_items(db, category, brand, season)]


@router.post("", response_model=ItemRead, status_code=201)
def create_item(data: ItemCreate, db: Session = Depends(get_db)):
    return serialize(crud.create_item(db, data))


@router.get("/{item_id}", response_model=ItemRead)
def get_item(item_id: int, db: Session = Depends(get_db)):
    item = crud.get_item(db, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return serialize(item)


@router.patch("/{item_id}", response_model=ItemRead)
def update_item(item_id: int, data: ItemUpdate, db: Session = Depends(get_db)):
    item = crud.get_item(db, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return serialize(crud.update_item(db, item, data))


@router.delete("/{item_id}", status_code=204)
def delete_item(item_id: int, db: Session = Depends(get_db)):
    item = crud.get_item(db, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    crud.delete_item(db, item)
