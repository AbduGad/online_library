#!/usr/bin/python3
"""
initialize the models package
"""

from os import getenv
from models.engine.db_storage import DBStorage

dataBase_name = "test_db" if getenv('test_db') == "true" else "online_lib"

storage = DBStorage(
    "storage",
    database_name=dataBase_name,
    check_create_database=True,

)
storage.reload()
