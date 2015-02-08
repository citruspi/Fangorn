from . import AuthenticatedResource, Resource, Folder
from flask import g, abort, request

class FolderResource(AuthenticatedResource):

    def post(self):

        name = request.form.get('name')

        if not name:

            abort(400)

        name = name.encode('utf-8')

        folders = [folder.name for folder in g.user.folders]

        if name in folders:

            abort(409)

        else:

            folder = Folder.create(
                    name = name,
                    user = g.user)

            return {'folders': [{
                        'id': f.id,
                        'name': f.name} for f in g.user.folders]}

    def get(self):

        return {'folders': [{
                    'id': f.id,
                    'name': f.name} for f in g.user.folders]}
