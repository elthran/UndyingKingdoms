from flask import jsonify
from flask.views import MethodView
from flask_login import login_required, current_user

from ..models import Token


# Consider moving this to the admin panel?
class TokenAPI(MethodView):
    @login_required
    def get(self):
        if current_user.is_admin:
            token = Token.encode_auth_token()
            if isinstance(token.decode(), str):
                return jsonify(
                    status='success',
                    message='You logged in and are and Admin user, so here is your token',
                    auth_token=token.decode()
                ), 200
            else:
                return jsonify(
                    status='fail',
                    message='token code is broken',
                    error=str(token)
                ), 200
        return jsonify(
            status='fail',
            message="You don't have authorization to generate a new token."
        ), 407
