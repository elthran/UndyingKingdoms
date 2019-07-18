from lib.routing_utils import import_endpoints
from app.api import api_blueprint

import_endpoints(
    api_blueprint,
    __name__,
    {
        'threads': None,
        'posts': None,
        'routing': None,
        'replies': None,
        'messaging': None,
        'upvote': {
            'path_args': '/<int:post_id>'
        },
    }
)
