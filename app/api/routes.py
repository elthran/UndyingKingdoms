"""
A configurable master list of all routes in the app.

"""
from app import api
from lib.controller_utils import add_all_controllers_in_package_to_namespace
from lib.http_verbs import *

add_all_controllers_in_package_to_namespace(api, globals())

# noinspection PyUnresolvedReferences
routes = {
    '/infrastructure': {
        GET: InfrastructureController.read,
        PUT: InfrastructureController.update,
    },
    '/navbar': {
        GET: NavbarController.read,
    },
    '/routing/<route>': {
        GET: RoutingController.read,
    },
}
