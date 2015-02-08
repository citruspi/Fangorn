from flask import request, abort, g
from . import User, Resource
import bcrypt

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

        return user.serializeToJSON()
