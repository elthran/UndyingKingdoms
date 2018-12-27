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
        # import pdb;pdb.set_trace()
        data = city_reader.get(ip)
        current_app.logger.info("Country: " + repr(data['country']['iso_code']))
        current_app.logger.info("Subdivisions: " + repr([division['names']['en'] for division in data['subdivisions']]))
        current_app.logger.info("City: " + repr(data['city']['names']['en']))
        # Store in User object?
    except TypeError:
        current_app.logger.info("Location: Not Found")
    finally:
        city_reader.close()
        return None  # Must return None or the request won't propagate.


@geo_ip.route('/geo_ip/update')
def update_geo_ip_database():
    import urllib.request
    import shutil
    import tarfile

    # first check if current file is up to date

    # if not download the new version

    # if that succeeds delete the old one

    # replace with new one and update file paths
    base_name = 'GeoLite2-City.tar.gz'
    geo_url = 'https://geolite.maxmind.com/download/geoip/database/' + base_name
    tmp_tar_gz = '/tmp/' + base_name
    with urllib.request.urlopen(geo_url) as f_in:
        with open(tmp_tar_gz, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)

    tar = tarfile.open(tmp_tar_gz, "r:gz")
    tar.extractall('/tmp/')

    return "Geo-location database has been updated."

