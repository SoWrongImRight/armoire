from typing import Optional

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.db.models import Item
from app.schemas.item import ItemCreate, ItemUpdate


def create_item(db: Session, data: ItemCreate) -> Item:
    item = Item(**data.model_dump())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


def get_item(db: Session, item_id: int) -> Optional[Item]:
    return db.get(Item, item_id)


def list_items(
    db: Session,
    category: Optional[str] = None,
    brand: Optional[str] = None,
    season: Optional[str] = None,
) -> list[Item]:
    query = db.query(Item)
    if category:
        query = query.filter(Item.category == category)
    if brand:
        query = query.filter(Item.brand == brand)
    if season:
        query = query.filter(Item.season == season)
    return query.order_by(Item.created_at.desc()).all()


def update_item(db: Session, item: Item, data: ItemUpdate) -> Item:
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(item, field, value)
    db.commit()
    db.refresh(item)
    return item


def delete_item(db: Session, item: Item) -> None:
    db.delete(item)
    db.commit()


def composition_summary(db: Session) -> dict:
    def counts_by(column):
        rows = (
            db.query(column, func.count(Item.id))
            .group_by(column)
            .all()
        )
        return {(key or "unspecified"): count for key, count in rows}

    return {
        "total": db.query(func.count(Item.id)).scalar() or 0,
        "by_category": counts_by(Item.category),
        "by_season": counts_by(Item.season),
        "by_brand": counts_by(Item.brand),
    }
