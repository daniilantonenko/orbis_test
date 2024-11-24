import os
from datetime import datetime
from fastapi import UploadFile
from src.models import FileModel

def save_file(file: UploadFile, upload_dir: str):
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)
    file_path = os.path.join(upload_dir, file.filename)
    with open(file_path, "wb") as f:
        f.write(file.file.read())
    
    return {
        "name": os.path.splitext(file.filename)[0],
        "extension": os.path.splitext(file.filename)[1],
        "size": os.path.getsize(file_path),
        "path": upload_dir,
        "created_at": datetime.now().isoformat()
    }

def delete_file(file_path: str):
    try: 
        if exists_file(file_path):
            os.remove(file_path)
    except Exception as e:
        print(e)

def get_filepath(file_record):
    file_path = os.path.join(file_record.path, f"{file_record.name}{file_record.extension}")
    if not exists_file(file_path):
        raise None    
    return file_path

def make_dir(dir_name: str):
    os.makedirs(dir_name, exist_ok=True)

def exists_file(file_path: str):
    return os.path.exists(file_path)

def rename_file(file_path: str, new_name: str):
    new_file_path = os.path.join(os.path.dirname(file_path), f"{new_name}{os.path.splitext(file_path)[1]}")
    os.rename(file_path, new_file_path)

def move_file(file_path: str, new_path: str):
    new_file_path = os.path.join(new_path, os.path.basename(file_path))
    os.rename(file_path, new_file_path)
    
def sync_filesystem_with_db(upload_dir):
    """
    Синхронизация базы данных и файловой системы.
    :param upload_dir: Директория хранения файлов.
    """
    # Получение списка файлов в хранилище
    existing_files = {
        os.path.join(root, file)
        for root, _, files in os.walk(upload_dir)
        for file in files
    }

    # Проверка файлов из базы данных
    db_files = {
        os.path.join(file_record.path, f"{file_record.name}{file_record.extension}")
        for file_record in FileModel.select()
    }

    # Удалить записи о файлах, которых нет в файловой системе
    missing_files = db_files - existing_files
    for file_path in missing_files:
        file_record = FileModel.get_or_none(path=os.path.dirname(file_path), name=os.path.splitext(os.path.basename(file_path))[0])
        if file_record:
            file_record.delete_instance()

    # Добавить записи в базу данных для файлов, которых нет в базе данных
    new_files = existing_files - db_files
    for file_path in new_files:
        file_stats = os.stat(file_path)
        FileModel.create(
            name=os.path.splitext(os.path.basename(file_path))[0],
            extension=os.path.splitext(file_path)[1],
            size=file_stats.st_size,
            path=os.path.dirname(file_path),
            created_at=datetime.fromtimestamp(file_stats.st_ctime).isoformat(),
        )