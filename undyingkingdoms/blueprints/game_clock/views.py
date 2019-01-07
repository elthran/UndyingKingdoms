from flask import jsonify, request, current_app
from flask.views import MethodView
from flask_login import login_required, current_user

from .models import Token


class AdvanceAPI(MethodView):
    def get(self):
        # get the auth token
        auth_header = request.headers.get('Authorization')
        if auth_header:
            try:
                auth_token = auth_header.split(" ")[1]
            except IndexError:
                response = {
                    'status': 'fail',
                    'message': 'Bearer token malformed.'
                }
                return jsonify(response), 401
        else:
            auth_token = ''
        if auth_token:
            resp = Token.decode_auth_token(auth_token)
            if not isinstance(resp, str) and resp == current_app.config.get("CLOCK_KEY"):
                response = {
                    'status': 'success',
                    'message': 'Oh happy day!'
                }
                return jsonify(response), 200
            response = {
                'status': 'fail',
                'message': resp
            }
            return jsonify(response), 401
        else:
            response = {
                'status': 'fail',
                'message': 'Provide a valid auth token.'
            }
            return jsonify(response), 401


# Consider moving this to the admin panel?
class TokenAPI(MethodView):
    @login_required
    def get(self):
        if current_user.is_admin:
            token = Token.encode_auth_token()
            if isinstance(token.decode(), str):
                return jsonify(
                    status='success',
                    message=token.decode()
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
