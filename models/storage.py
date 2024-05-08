from models.engine.db_storage import DBStorage

storage = DBStorage(
    "storage",
    database_name="test_db",
    check_create_database=True,
)

storage.reload()
