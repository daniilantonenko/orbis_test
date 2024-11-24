import unittest

import os
import io
from datetime import datetime
from fastapi import UploadFile

from src.services import save_file, delete_file, sync_filesystem_with_db
from src.db import db

class TestServices(unittest.TestCase):  
    def test_save_file(self):
        filename = "test.txt"
        upload_dir = "test_dir_save" 
        file = UploadFile(filename=filename, file=io.BytesIO(b"test content"))

        result = save_file(file, upload_dir)

        self.assertEqual(result["name"], "test")
        self.assertEqual(result["extension"], ".txt")
        self.assertEqual(result["size"], 12)
        self.assertEqual(result["path"], upload_dir)
        self.assertEqual(result["created_at"], datetime.now().isoformat())

        # Удаление временного файла
        os.remove(os.path.join(upload_dir, filename))
        os.rmdir(upload_dir)

    def test_delete_file(self):
        filename = "test.txt"
        upload_dir = "test_dir_delete" 
        # Создание временного файла
        file = UploadFile(filename=filename, file=io.BytesIO(b"test content"))
        os.makedirs(upload_dir, exist_ok=True)
        file_path = os.path.join(upload_dir, filename)

        delete_file(file_path)

        self.assertFalse(os.path.exists(file_path))

        # Удаление временного файла
        os.rmdir(upload_dir)