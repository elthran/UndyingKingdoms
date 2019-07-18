from flask import jsonify, url_for, request
from werkzeug.routing import BuildError

from lib.base_controller import CRUDMethodView


class RoutingController(CRUDMethodView):
    def read(self, route):
        if route == 'base':
            return jsonify(
                debugMessage="You requested the base url from the routing api.",
                base=request.url_root,
            ), 200
        try:
            path = url_for(route, **request.args)
            return jsonify(
                debugMessage="You called on the routing api.",
                base=request.url_root,
                path=path,
                # drop leading /
                url=request.url_root + path[1:]
            ), 200
        except BuildError as ex:
            return jsonify(
                debugMessage=str(ex)
            ), 404
