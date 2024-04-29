#!/usr/bin/python
""" holds class City"""
import models
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String, ForeignKey, Integer
from sqlalchemy.orm import relationship
from user import user_library_association


class Book(BaseModel, Base):
    __tablename__ = 'books'

    name = Column(String(100))
    author = Column(String(100))
    #tags = Column(String(100))

    # Define many-to-many relationship with User
    #users = relationship("User", secondary=user_library_association, back_populates="library")

    def __init__(self, *args, **kwargs):
        """initializes city"""
        
        super().__init__(*args, **kwargs)
