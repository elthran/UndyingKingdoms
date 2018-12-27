import os

import maxminddb
from flask import Blueprint, request, current_app

# causes import loop, need to refactor model design
# from undyingkingdoms.models.users import User

geo_ip = Blueprint('geoip', __name__)


@geo_ip.before_app_request
def pull_ip_hook():
    # import pdb;pdb.set_trace()
    city_reader = maxminddb.open_database(os.path.join(current_app.static_folder, 'GeoLite2-City_20181218', 'GeoLite2-City.mmdb'))
    # optionally url_for('static' + 'GeoLite2-Country.mmdb')
    current_app.logger.info("Remote IP: " + repr(request.remote_addr))
    current_app.logger.info("Access route: " + repr(request.access_route))
    try:
        ip = request.access_route[0]
        import pdb;pdb.set_trace()
        data = city_reader.get(ip)
        current_app.logger.info("Country: " + repr(data['country']['iso_code']))
        current_app.logger.info("Subdivisions: " + repr([division['names']['en'] for division in data['subdivisions']]))
        current_app.logger.info("City: " + repr(data['city']['names']['en']))
        # Store in User object?
    except TypeError:
        current_app.logger.info("Location: Not Found")
    finally:
        city_reader.close()
    return None  # Must return None or the request won't propogate.
