from ..helpers import import_endpoints
from ... import api_blueprint

import_endpoints(
    api_blueprint,
    __name__,
    [
        'basics',
        'county_description',
        'treasury',
        'citizens',
        'news'
    ]
)

