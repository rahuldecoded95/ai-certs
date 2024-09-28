from flask import Blueprint
from flask_restful import Api
#
from global_utilities import app
#
from resources.upload import Upload


base_route = "/api"
upload_blueprint = Blueprint('upload_blueprint', __name__, url_prefix=base_route)
upload_api = Api(upload_blueprint)

app.logger.info(f"Registering resource for api: endpoint: {base_route}/upload")
upload_api.add_resource(
    Upload,
    '/upload',
    endpoint="upload"
)

app.register_blueprint(upload_blueprint)