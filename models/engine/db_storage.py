#!/usr/bin/python3
"""
Contains the class DBStorage
"""

import models
from models.base_model import BaseModel, Base
from models.book import Books
from models.book_tags import Books_tags
from models.tags import Tags
from models.book import Books

from os import getenv
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

available_classes = {
    "Books": Books,
    "tags": Tags,
    "Books_tags": Books_tags,
}

association_tables = {"Books_tags": Books_tags}


class DBStorage:
    """interaacts with the MySQL database"""
    __engine = None
    __session: scoped_session = None

    def __init__(self, test=False):
        """Instantiate a DBStorage object"""
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.
                                      format("abdo",
                                             "ebdo",
                                             "localhost",
                                             "online_lib"), echo=True)
        if True == test:
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """query on the current database session"""
        new_dict = {}
        for key in available_classes:
            if (cls is None or cls is available_classes[key]
                    or cls is key) and cls not in association_tables.values():

                objs = self.__session.query(available_classes[key]).all()
                for obj in objs:
                    key = obj.__class__.__name__ + '.' + str(obj.id)
                    new_dict[key] = obj
        return (new_dict)

    def new(self, obj):
        """add the object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """commit all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """delete from the current database session obj if not None"""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """reloads data from the database"""
        Base.metadata.create_all(self.__engine)
        sess_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(sess_factory)
        self.__session = Session

    def close(self):
        """call remove() method on the private session attribute"""
        self.__session.remove()

    def get(self, cls, id):
        """
        Returns the object based on the class name and its ID, or
        None if not found
        """
        if cls not in available_classes.values():
            return None

        all_cls = models.storage.all(cls)
        for value in all_cls.values():
            if (value.id == id):
                return value

        return None

    def getBy_name(self, cls: BaseModel, name):
        """
        Returns the object based on the class name, or
        None if not found
        """
        if cls not in available_classes.values():
            return None

        result = self.__session.query(cls).filter(
            cls.name.in_([name]))

        return result.scalar()

    def count(self, cls=None):
        """
        count the number of objects in storage
        """
        all_class = available_classes.values()

        if not cls:
            count = 0
            for clas in all_class:
                count += len(models.storage.all(clas).values())
        else:
            count = len(models.storage.all(cls).values())

        return count
