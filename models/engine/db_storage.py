#!/usr/bin/python3
"""
Contains the class DBStorage
"""
from models.base_model import BaseModel, Base
from models.book import Books
from models.book_tags import Books_tags
from models.tags import Tags
from models.book import Books
from models.user_support_messages import User_support
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy import MetaData


available_classes = {
    "Books": Books,
    "tags": Tags,
    "Books_tags": Books_tags,
    "User_support": User_support 
}

association_tables = {"Books_tags": Books_tags}


class DBStorage:
    """interaacts with the MySQL database"""
    __engine = None
    __session: scoped_session = None

    def __init__(
            self, instance_name,
            database_name,
            test=False,
            check_create_database=False, ):
        """Instantiate a DBStorage object"""
        self.dataBase_name = database_name
        self.instance_name = instance_name

        db_uri = 'mysql+mysqldb://{}:{}@{}/{}'.format("root",
                                                      "123",
                                                      "localhost",
                                                      self.dataBase_name)

        self.__engine = create_engine(db_uri, echo=False)
        # self.session_factory = None

        if check_create_database is True:
            if not database_exists(self.__engine.url):
                # Create the database
                create_database(self.__engine.url)
                print("Database created successfully")
            else:
                print("Database already exists")

    def all(self, cls=None):
        """query on the current database session"""
        new_dict = {}

        self.cls_validate(cls)

        for key in available_classes:
            # print(
            #     (cls is None or cls is available_classes[key]
            # or cls is key) and cls key in association_tables.values(), key)

            if (cls is None or cls is available_classes[key] or cls is key) and \
                    available_classes[key] not in association_tables.values():

                objs = self.__session.query(available_classes[key]).all()

                for obj in objs:
                    key = obj.__class__.__name__ + '.' + str(obj.id)
                    new_dict[key] = obj

        return (new_dict)

    def new(self, cls):
        """add the object to the current database session"""
        self.subclass_instance_validate(cls, null_safety=True)
        if cls is None:
            # print("value error (in db_stroge new function)")
            raise ValueError("none value")
        # if cls is not None and not any(isinstance(cls, obj)
        #                                for obj in available_classes.values()):
        #     raise TypeError(f"({cls} ,{type(cls)}) is not supported")
        self.__session.add(cls)

    def save(self):
        """commit all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """delete from the current database session obj if not None"""
        self.subclass_instance_validate(obj, null_safety=True)

        self.__session.delete(obj)

    def reload(self):
        """reloads data from the database"""
        Base.metadata.create_all(self.__engine)

        session_factory = sessionmaker(
            bind=self.__engine, expire_on_commit=False)

        Session = scoped_session(session_factory)

        self.__session = Session

    def close(self):
        """call remove() method on the private session attribute"""
        # self.session_factory.close_all()
        self.__session.remove()

        # self.__session.close_all()

    def get(self, cls: BaseModel, id):
        """
        Returns the object based on the class name and its ID, or
        None if not found
        """
        if cls is None:
            return None

        self.cls_validate(cls, null_safety=False)

        result = self.__session.query(cls).filter(
            cls.id == str(id))
        return result.scalar()

    def getBy_name(self, cls: BaseModel, name):
        """
        Returns the object based on the class name, or
        None if not found
        """
        if cls is None:
            return None

        self.cls_validate(cls, null_safety=False)

        # print(
        #     "going innnnnnnnnnnnnnn",
        #     self.instance_name,
        #     name,
        #     self.__dict__)

        result = self.__session.query(cls).filter(
            cls.name == name)
        # all_cls = self.all(cls)
        # for value in all_cls.values():
        #     if (value.name == name):
        #         if value is not None and value.name is not None:
        #             print("going outtttttt", value.name)
        #         return value

        # if result is not None and result.first() is not None:
        #     print("going outtttttt", result.first().name)

        return result.scalar()

    def count(self, cls=None):
        """
        count the number of the givin class in storage ,if the givin
        obj is null , return number of all the objects in the storage
        """
        all_class = available_classes.values()
        self.cls_validate(cls)

        if not cls:
            count = 0
            for cls_obj in all_class:
                count += len(self.all(cls_obj).values())
        else:
            count = len(self.all(cls).values())

        return count

    def subclass_instance_validate(self, cls, null_safety=False):
        if null_safety is True and cls is None:
            raise ValueError(f"the object is a null value")

        if cls is not None and not any(isinstance(cls, obj)
                                       for obj in available_classes.values()):
            raise TypeError(f"({cls} ,{type(cls)}) is not supported")

    def cls_validate(self, cls, null_safety=False):

        if null_safety is True and cls is None:
            raise ValueError(f"the object is a null value")

        if (cls is not None) and \
                (cls not in available_classes.values()):
            raise TypeError(f"({cls} ,{type(cls)}) is not supported")

    def drop_dataBase(self):
        Base.metadata.drop_all(self.__engine)
