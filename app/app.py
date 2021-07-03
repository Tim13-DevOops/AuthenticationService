import os

from flask import Flask

# from flask.wrappers import Response
from flask_restful import Api
from flask_migrate import Migrate
from flask_migrate import init as migrate_init
from flask_migrate import migrate as migrate_migrate
from flask_migrate import upgrade as migrate_upgrade
from flask_cors import CORS
import app.config as config
from datetime import datetime

# import json
from app.repository.database import init_database


app = Flask(__name__)
app.config["SECRET_KEY"] = config.FLASK_SECRET_KEY
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


cors = CORS(app, resources={r"/*": {"origins": "*"}})

api = Api(app)
db = init_database(app)

from app.rbac import rbac

rbac.setJWTManager(app)

# @app.errorhandler(Exception)
# def handle_exception(error):
#     response = Response()
#     response.data = json.dumps(
#         {
#             "code": 500,
#             "name": "Internal server error",
#         }
#     )
#     response.status_code = 500
#     response.content_type = "application/json"
#     return response


migrate = Migrate(app, db)

from app.api.user_api import (
    UserAPI,
    LoginAPI,
    BanUserAPI,
    ResolveAgentRequestAPI,
)
from app.repository.user import AppUser, populate_admins

api.add_resource(UserAPI, "/user")
api.add_resource(LoginAPI, "/login")
api.add_resource(BanUserAPI, "/user/<int:user_id>/ban")
api.add_resource(ResolveAgentRequestAPI, "/user/<int:user_id>/agent_request")




def db_migrate():
    with app.app_context():
        if not os.path.exists("./migrations"):
            migrate_init()
        migrate_migrate()
        migrate_upgrade()


def main():
    populate_admins()
    app.run(host="0.0.0.0", debug=True)


if __name__ == "__main__":
    main()
