from flask import Flask
from flask.ext.restful import Api, Resource
from peewee import SqliteDatabase

database = SqliteDatabase('/tmp/fangorn.db', threadlocals=True)

from models import User, Token, Folder, File

database.create_tables([User, Token, Folder, File], True)

app = Flask(__name__)
api = Api(app)

from users import RegistrationResource, AuthenticationResource, AuthenticatedResource
from folders import FolderResource, FolderInstance

api.add_resource(RegistrationResource, '/users/')
api.add_resource(AuthenticationResource, '/authenticate/')
api.add_resource(FolderResource, '/folders/')
api.add_resource(FolderInstance, '/folders/<int:id>/')
