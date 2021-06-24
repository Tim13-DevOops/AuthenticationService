from flask_restful import Resource
from flask import request, jsonify

# from rbac import rbac
from app.services import user_service


class UserAPI(Resource):
    # method_decorators = [rbac.Allow(['admin'])]
    def get(self):
        return jsonify(user_service.get_users())

    def post(self):
        """
        user_dict:
            username: str
            password: str
            user_role: 'user' or 'agent'
            name: str
            surname: str
            email: str
            phone_number: str
            website: str
        """
        user_dict = request.get_json()
        user = user_service.register(user_dict)
        return jsonify(user)

    def put(self):
        user_dict = request.get_json()
        user = user_service.update_user(user_dict)
        return jsonify(user)


class LoginAPI(Resource):
    def post(self):
        """
        login_dict:
            username: str
            password: str
        """
        token = user_service.login(request.get_json())
        return jsonify(token)


class SingleUserAPI(Resource):
    def delete(self, user_id):
        return jsonify(user_service.delete_user(user_id))


class BanUserAPI(Resource):
    def post(self, user_id):
        return jsonify(user_service.ban_user(user_id))


class ResolveAgentRequestAPI(Resource):
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
