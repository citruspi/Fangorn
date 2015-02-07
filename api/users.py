from flask import request, abort, g
from . import User, Resource
import bcrypt

class RegistrationResource(Resource):

    def post(self):

        firstname = request.form.get('firstname').encode('utf-8')
        lastname = request.form.get('lastname').encode('utf-8')
        username = request.form.get('username').encode('utf-8')
        email = request.form.get('email').encode('utf-8')
        password = request.form.get('password').encode('utf-8')

        if (not firstname or not lastname or not username or not email or not
                password):

            abort(400)

        if User.select().where(User.username == username).count() == 1:

            abort(409)

        if User.select().where(User.email == email).count() == 1:

            abort(409)

        user = User.create(
                firstname = firstname,
                lastname = lastname,
                username = username,
                email = email,
                password = bcrypt.hashpw(password, bcrypt.gensalt()))

        return {
                'id': user.id,
                'firstname': user.firstname,
                'lastname': user.lastname,
                'username': user.username,
                'email': user.email
               }
