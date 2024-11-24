from peewee import Model, CharField, IntegerField, DateTimeField, TextField
from pydantic_settings import BaseSettings

class FileModel(Model):
    name = CharField()
    extension = CharField()
    size = IntegerField()
    path = CharField()
    created_at = DateTimeField()
    updated_at = DateTimeField(null=True)
    comment = TextField(null=True)