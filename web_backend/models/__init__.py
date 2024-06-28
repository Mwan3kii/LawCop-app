#!/usr/bin/python3
"""initialize the models package"""

from os import getenv


storage_t = getenv("LC_TYPE_STORAGE")

if storage_t == "db":
    print("storage from database")
    from models.storages.db_storage import DBStorage
    storage = DBStorage()
else:
    print("frome file")
    from models.storages.file_storage import FileStorage
    storage = FileStorage()
storage.reload()
