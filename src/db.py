from peewee import SqliteDatabase
from src.models import FileModel

from src.config import  DATABASE

# Настройка базы данных
db = SqliteDatabase(DATABASE["db_name"])

# Установка соединения с базой данных
FileModel._meta.database = db

# Зависимость для подключения к базе данных
def get_db():
    try:
        db.connect()
        db.create_tables([FileModel]) 
        yield
    finally:
        if not db.is_closed():
            db.close()