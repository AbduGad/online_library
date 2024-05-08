#!/usr/bin/python3
"""
Contains class BaseModel
"""

from datetime import datetime
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String, DateTime, Index
from sqlalchemy.ext.declarative import declarative_base
import uuid

time = "%Y-%m-%dT%H:%M:%S.%f"


Base = declarative_base()


class BaseModel:
    __tablename__ = "BaseModel"
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow())
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow())
    id = Column(
        String(60),
        nullable=False,
        default=uuid.uuid4,
        primary_key=True)

    def __init__(self, *args, **kwargs):
        if kwargs:
            for att, Value in kwargs.items():
                # if key != '__class__':
                setattr(self, att, Value)

    def __str__(self):
        """Returns a string representation of the instance"""
        cls = (str(type(self)).split('.')[-1]).split('\'')[0]
        return '[{}] ({}) {}'.format(cls, self.id, self.__dict__)

    def delete(self):
        """Deletes this BaseModel instance from the storage"""
        from models import storage
        storage.delete(self)

    def save(self):
        """Updates updated_at with current time when instance is changed"""
        from models import storage
        self.updated_at = datetime.now()
        storage.new(self)
        storage.save()

    def to_dict(self):
        """Convert instance into dict format"""
        dictionary = {}
        for key, value in self.__dict__.items():
            if key != '_sa_instance_state':
                if isinstance(value, datetime):
                    dictionary[key] = value.isoformat()
                else:
                    dictionary[key] = value
        dictionary['__class__'] = self.__class__.__name__
        return dictionary
