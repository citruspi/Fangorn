from flask import request, abort, g
from . import User, Token, Resource
import bcrypt
import os

class AuthenticationResource(Resource):

    def post(self):

        username = request.form.get('username')
        password = request.form.get('password')

        def verify (username, password):

            try:

                user = User.get(User.username == username)
                computed = user.password.encode('utf-8')

                if bcrypt.hashpw(password, computed) == computed:
                    return True

            except User.DoesNotExist:

                pass

            return False

        if not username or not password:

            abort(400)

        username = username.encode('utf-8').lower()
        password = password.encode('utf-8')

        if not verify(username, password):

            abort(401)

        else:

            user = User.get(User.username == username)

            token = Token.create(
                    token = Token.generateToken(),
                    user = user)

            return {'token': token.token}

class RegistrationResource(Resource):

    def post(self):

        firstname = request.form.get('firstname')
        lastname = request.form.get('lastname')
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        if (not firstname or not lastname or not username or not email or not
                password):

            abort(400)

        firstname = firstname.encode('utf-8')
        lastname = lastname.encode('utf-8')
        username = username.encode('utf-8').lower()
        email = email.encode('utf-8').lower()
        password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        if User.select().where(User.username == username).count() == 1:

            abort(409)

        if User.select().where(User.email == email).count() == 1:

            abort(409)

        user = User.create(
                firstname = firstname,
                lastname = lastname,
                username = username,
                email = email,
                password = password)

        token = Token.create(
                token = Token.generateToken(),
                user = user)

        response = user.serializeToJSON()
        response['tokens'] = [token.token]

        return response
