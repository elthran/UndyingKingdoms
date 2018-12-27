import os

import maxminddb
from flask import Blueprint, request, current_app

# causes import loop, need to refactor model design
# from undyingkingdoms.models.users import User

geo_ip = Blueprint('geoip', __name__)


@geo_ip.before_app_request
def pull_ip_hook():
    # import pdb;pdb.set_trace()
    reader = maxminddb.open_database(os.path.join(current_app.static_folder, 'GeoLite2-Country_20181218', 'GeoLite2-Country.mmdb'))
    # optionally url_for('static' + 'GeoLite2-Country.mmdb')
    current_app.logger.info("Remote IP: " + repr(request.remote_addr))
    current_app.logger.info("Access route: " + repr(request.access_route))
    try:
        data = reader.get(request.remote_addr)
        current_app.logger.info("Country data: " + repr(data))
        # Store in User object?
    finally:
        reader.close()
    return None  # Must return None or the request won't propogate.
