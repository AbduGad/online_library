#!/usr/bin/python
""" holds class Amenity"""
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from sqlalchemy import UniqueConstraint


class Tags(BaseModel, Base):
    """Representation of Amenity """
    __table_args__ = (UniqueConstraint("name", name='tag_name'),)

    __tablename__ = 'tags'
    name = Column("name", String(128), nullable=False, unique=True)

    books = relationship(
        "Books",
        secondary="book_tags",
        back_populates="tags",
    )

    def __init__(self, *args, **kwargs):
        """initializes Amenity"""
        super().__init__(*args, **kwargs)
