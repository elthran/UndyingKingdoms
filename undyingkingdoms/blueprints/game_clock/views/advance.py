from flask import request, jsonify, current_app
from flask.views import MethodView

from ..models import Token
from undyingkingdoms.models import World


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
            if resp == current_app.config.get("CLOCK_KEY"):

                # advance game clock here!
                world = World.query.first()
                world.advance_day()

                response = {
                    'status': 'success',
                    'message': 'Oh happy day!'
                }
                return jsonify(response), 200
            response = {
                'status': 'fail',
                'message': "Response token doesn't match private_config.CLOCK_KEY."
            }
            return jsonify(response), 401
        else:
            response = {
                'status': 'fail',
                'message': 'Provide a valid auth token.'
            }
            return jsonify(response), 401
