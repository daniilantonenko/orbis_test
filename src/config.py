import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Конфигурация базы данных
DATABASE = {
    "db_name": os.getenv("DB_NAME", "files.db"),
}


# Конфигурация базы данных
APP = {
    "upload_dir": os.getenv("UPLOAD_DIR", os.path.join(BASE_DIR, "storage")),
}