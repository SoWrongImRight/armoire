from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String

from app.db.database import Base


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    category = Column(String, nullable=False, index=True)
    brand = Column(String, nullable=True, index=True)
    season = Column(String, nullable=True, index=True)
    fit = Column(String, nullable=True)
    size = Column(String, nullable=True)
    color = Column(String, nullable=True)
    image_key = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
