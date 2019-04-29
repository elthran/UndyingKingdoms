from undyingkingdoms.api.helpers import import_endpoints
from undyingkingdoms.api import api_blueprint

import_endpoints(
    api_blueprint,
    __name__,
    [
        'population',
        'gold',
        'food',
        'wood',
        'iron',
        'stone',
        'mana',
        'happiness',
        'nourishment',
        'health',
        'update'
    ]
)

