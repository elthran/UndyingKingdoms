from flask import jsonify

from lib.base_controller import CRUDMethodView


class FakeController(CRUDMethodView):
    def string_response(self):
        return 'foo'

    def string_with_status_response(self):
        return 'bar', 201

    def dictionary_response(self):
        return dict(foo='foo')

    def dictionary_with_status_response(self):
        return dict(foo='foo'), 201

    def json_response(self):
        return jsonify(bar='bar')

    def json_with_status_response(self):
        return jsonify(bar='bar'), 201

    def null_response(self):
        pass
