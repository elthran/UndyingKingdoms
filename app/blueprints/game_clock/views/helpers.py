import functools

from flask import request, jsonify, current_app

from ..models import Token


def check_clock_key(func):
    """Implement bearer token checking on any function."""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
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

                # IMPORTANT
                # Execute primary function.
                if func(*args, **kwargs) is not None:
                    raise Exception("You function shouldn't return anything!")

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
    return wrapper
