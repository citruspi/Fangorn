import datetime
from peewee import *
from . import database
import os
import bcrypt

class User(Model):

    firstname = CharField()
    lastname = CharField()
    username = CharField()
    email = CharField()
    password = CharField()

    @staticmethod
    def authenticate(username, password):

        try:

            user = User.get(User.username == username)
            computed = user.password.encode('utf-8')

            if bcrypt.hashpw(password, computed) == computed:
                return True

        except User.DoesNotExist:
            pass

        return False

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

    @staticmethod
    def generateToken():

        token = os.urandom(64).encode('hex')
        while Token.select().where(Token.token == token).count() != 0:
            token = os.urandom(64).encode('hex')

        return token

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

