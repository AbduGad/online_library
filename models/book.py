#!/usr/bin/python
""" holds class City"""
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String, ForeignKey, Integer, Index
from sqlalchemy.orm import relationship
import os
import sys
# from user import user_library_association


class Books(BaseModel, Base):
    __tablename__ = 'books'

    name = Column(String(100), nullable=False)
    author = Column(String(100), nullable=False)
    path = Column(String(100), nullable=False)

    cover_img_path = Column(
        String(100),
        nullable=False,
        default=r"pdf_images/test_image.jpeg")

    author_summary = Column(
        String(1000),
        nullable=False,
        default="great writer lives in egypt")

    author_img_path = Column(
        String(100),
        nullable=False,
        default=r"pdf_images/author.png")

    tags = relationship("Tags", secondary="book_tags", back_populates="books")

    __table_args__ = (
        Index('idx_books_name', name),  # Add this line
    )
# Define many-to-many relationship with User
# users = relationship("User", secondary=user_library_association,
# back_populates="library")

    def __init__(self, *args, **kwargs):
        """initializes Book"""
        book_name = kwargs.get("name")

        if book_name is not None:
            root_directory = os.path.dirname(os.path.dirname(__file__))
            pdf_directory = os.path.join(root_directory, "pdf")
            self.path = os.path.join(pdf_directory, book_name)

        super().__init__(*args, **kwargs)
