from peewee import SqliteDatabase

database = SqliteDatabase('/tmp/fangorn.db', threadlocals=True)

from models import User, Token, Folder, File

database.create_tables([User, Token, Folder, File], True)

