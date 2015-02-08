import datetime
from peewee import *
from . import database

class User(Model):

    firstname = CharField()
    lastname = CharField()
    username = CharField()
    email = CharField()
    password = CharField()

    def serializeToJSON(self):

        return {
                'id': self.id,
                'firstname': self.firstname,
                'lastname': self.lastname,
                'username': self.username,
                'email': self.email,
               }

    class Meta:

        database = database

class Token(Model):

    token = CharField()
    user = ForeignKeyField(User, related_name='tokens')

    class Meta:

        database = database

class Folder(Model):

    name = CharField()
    user = ForeignKeyField(User, related_name='folders')

    class Meta:

        database = database

class File(Model):

    name = CharField()
    status = CharField()
    timestamp = DateTimeField(default=datetime.datetime.now)
    location = CharField()
    tags = CharField()
    description = TextField()
    size = IntegerField()
    kind = CharField()
    folder = ForeignKeyField(Folder, related_name='files')

    class Meta:

        database = database

