#!/usr/bin/python
""" holds class City"""
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String, ForeignKey, Integer, Index
from sqlalchemy.orm import relationship
# from user import user_library_association


class Books(BaseModel, Base):
    __tablename__ = 'books'

    name = Column(String(100), nullable=False)
    author = Column(String(100), nullable=False)
    path = Column(String(100), nullable=False)
    tags = relationship("Tags", secondary="book_tags", back_populates="books")
    __table_args__ = (
        Index('idx_books_name', name),  # Add this line
    )
# Define many-to-many relationship with User
# users = relationship("User", secondary=user_library_association,
# back_populates="library")

    def __init__(self, *args, **kwargs):
        """initializes Book"""
        super().__init__(*args, **kwargs)
