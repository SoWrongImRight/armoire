from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class ItemBase(BaseModel):
    name: str
    category: str
    brand: Optional[str] = None
    season: Optional[str] = None
    fit: Optional[str] = None
    size: Optional[str] = None
    color: Optional[str] = None
    image_key: Optional[str] = None


class ItemCreate(ItemBase):
    pass


class ItemUpdate(BaseModel):
    name: Optional[str] = None
    category: Optional[str] = None
    brand: Optional[str] = None
    season: Optional[str] = None
    fit: Optional[str] = None
    size: Optional[str] = None
    color: Optional[str] = None
    image_key: Optional[str] = None


class ItemRead(ItemBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    image_url: Optional[str] = None
    created_at: datetime
