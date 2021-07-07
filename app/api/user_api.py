from flask_restful import Resource
from flask import request, jsonify

from app.services import user_service
from app.rbac import rbac


class UserAPI(Resource):
    method_decorators = {
        "get": [rbac.Allow(["admin"])],
        "put": [rbac.Allow(["admin", "user", "agent"])],
        "delete": [rbac.Allow(["admin", "user", "agent"])],
    }

    def get(self):
        return jsonify(user_service.get_users())

    def post(self):
        """
        user_dict:
            username: str
            password: str
        """
        user_dict = request.get_json()
        user = user_service.register(user_dict)
        return jsonify(user)

    def put(self):
        user_dict = request.get_json()
        user = user_service.update_user(user_dict)
        return jsonify(user)

    def delete(self):
        return jsonify(user_service.delete_user())


class LoginAPI(Resource):
    def post(self):
        """
        login_dict:
            username: str
            password: str
        """
        login_dict = request.get_json()
        token = user_service.login(login_dict)
        return jsonify(token)


class BanUserAPI(Resource):
    method_decorators = [rbac.Allow(["admin"])]

    def post(self, user_id):
        return jsonify(user_service.ban_user(user_id))


class ResolveAgentRequestAPI(Resource):
    method_decorators = [rbac.Allow(["admin"])]

    def post(self, user_id):
        """
        Args:
            user_id: str
            request_dict:
                approve: bool
        """
        user_dict = request.get_json()
        approve = user_dict["approve"]
        return jsonify(user_service.resolve_agent_request(user_id, approve))
