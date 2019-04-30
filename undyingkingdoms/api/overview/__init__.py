from undyingkingdoms.api.helpers import import_endpoints
from undyingkingdoms.api import api_blueprint

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

