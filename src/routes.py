from playhouse.shortcuts import model_to_dict
from fastapi import UploadFile, HTTPException, Depends, APIRouter
from fastapi.responses import FileResponse
from datetime import datetime

from src.db import get_db
from src.models import FileModel
from src.services import save_file, delete_file, get_filepath, make_dir, exists_file, sync_filesystem_with_db, rename_file, move_file

from src.config import  APP

# Создание необходимых директорий
make_dir(APP["upload_dir"])

router = APIRouter()

@router.get("/")
async def root():
    return {"message": "Welcome to File Storage API!"}

@router.get("/files/")
async def get_files():
    """Получение списка всех файлов из базы данных."""
    files = [model_to_dict(file) for file in FileModel.select()]
    return {"files": files}

@router.get("/files/{file_id}")
async def get_file(file_id: int):
    """Получение информации о конкретном файле."""
    file_record = FileModel.get_or_none(id=file_id)
    if not file_record:
        raise HTTPException(status_code=404, detail="File not found")
    return model_to_dict(file_record)

@router.post("/upload/")
async def upload_file(file: UploadFile, db=Depends(get_db)):
    """Загрузка нового файла в хранилище."""

    print(file.filename)

    try:      
        file_data = save_file(file, APP["upload_dir"])

        FileModel.create(**file_data)
        return {"message": "File uploaded successfully", "file": file_data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/files/{file_id}")
async def delete_file(file_id: int, db=Depends(get_db)):
    """Удаление файла из базы данных и хранилища."""
    file_record = FileModel.get_or_none(id=file_id)
    if not file_record:
        raise HTTPException(status_code=404, detail="File not found")
    
    file_path = get_filepath(file_record)
    delete_file(file_path)

    if exists_file(file_path):
        raise HTTPException(status_code=500, detail="Failed to delete file")
    
    file_record.delete_instance()
    return {"message": "File deleted successfully"}

@router.get("/download/{file_id}")
async def download_file(file_id: int):
    """Скачивание файла из хранилища."""
    file_record = FileModel.get_or_none(id=file_id)
    if not file_record:
        raise HTTPException(status_code=404, detail="File not found")
    
    file_path = get_filepath(file_record)
    if file_path is None:
        raise HTTPException(status_code=404, detail="File not found in storage")
    
    return FileResponse(path=file_path, media_type="application/octet-stream", filename=file_record.name + file_record.extension)

@router.post("/sync/")
async def sync_database_with_files():
    """
    Эндпоинт для синхронизации базы данных и файловой системы.
    """
    try:
        sync_filesystem_with_db(APP["upload_dir"])
        return {"message": "Synchronization completed successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during synchronization: {str(e)}")
    
    
@router.put("/files/{file_id}")
async def update_file(file_id: int, db=Depends(get_db)):
    """Обновление информации о конкретном файле."""
    file_record = FileModel.get_or_none(id=file_id)
    if not file_record:
        raise HTTPException(status_code=404, detail="File not found")
    
    file_path = get_filepath(file_record)
    if file_path is None:
        raise HTTPException(status_code=404, detail="File not found in storage")
    
    try:
        file_data = save_file(file=file_record, upload_dir=APP["upload_dir"])
        file_record.updated_at = datetime.now().isoformat()
        file_record.update(**file_data).apply()
        return {"message": "File updated successfully", "file": file_data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.put("/files/{file_id}/comment")
async def update_file_comment(file_id: int, comment: str, db=Depends(get_db)):
    """Обновление комментария к файлу."""
    file_record = FileModel.get_or_none(id=file_id)
    if not file_record:
        raise HTTPException(status_code=404, detail="File not found")
    
    file_record.comment = comment
    file_record.updated_at = datetime.now().isoformat()
    file_record.save()

    return {"message": "Comment updated successfully"}

@router.put("/files/{file_id}/name")
async def update_file_name(file_id: int, name: str, db=Depends(get_db)):
    """Обновление комментария к файлу."""
    file_record = FileModel.get_or_none(id=file_id)
    if not file_record:
        raise HTTPException(status_code=404, detail="File not found")
    
    file_record.name = name
    file_record.updated_at = datetime.now().isoformat()
    file_record.save()

    file_path = get_filepath(file_record)
    rename_file(file_path, name)

    if not exists_file(file_path):
        raise HTTPException(status_code=500, detail="Failed to rename file")

    return {"message": "Comment updated successfully"}

@router.put("/files/{file_id}/name")
async def update_file_path(file_id: int, path: str, db=Depends(get_db)):
    """Обновление комментария к файлу."""
    file_record = FileModel.get_or_none(id=file_id)
    if not file_record:
        raise HTTPException(status_code=404, detail="File not found")
    
    file_record.path = path
    file_record.updated_at = datetime.now().isoformat()
    file_record.save()

    file_path = get_filepath(file_record)
    move_file(file_path, path)

    if not exists_file(file_path):
        raise HTTPException(status_code=500, detail="Failed to rename file")

    return {"message": "Comment updated successfully"}