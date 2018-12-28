import os

import maxminddb
from flask import Blueprint, request, current_app, url_for

# causes import loop, need to refactor model design
# from undyingkingdoms.models.users import User

geo_ip = Blueprint('geoip', __name__)

geo_ip_db = 'GeoLite2-City/GeoLite2-City.mmdb'


@geo_ip.before_app_request
def pull_ip_hook():
    # import pdb;pdb.set_trace()
    geo_ip_db_path = os.path.join(current_app.static_folder, geo_ip_db)
    # optionally
    current_app.logger.info("Remote IP: " + repr(request.remote_addr))
    current_app.logger.info("Access route: " + repr(request.access_route))
    ip = request.access_route[0]

    with maxminddb.open_database(geo_ip_db_path) as reader:
        data = reader.get(ip)
        try:
            current_app.logger.info("Country: " + repr(data['country']['iso_code']))
            current_app.logger.info("Subdivisions: " + repr([division['names']['en'] for division in data['subdivisions']]))
            current_app.logger.info("City: " + repr(data['city']['names']['en']))
            # Store in User object?
        except TypeError:
            current_app.logger.info("Location: Not Found")
    return None  # Must return None or the request won't propagate.


@geo_ip.route('/geo_ip/update')
def update_geo_ip_database():
    import urllib.request
    import shutil
    import tarfile
    from datetime import datetime, timedelta

    geo_ip_db_folder = os.path.join(current_app.static_folder, 'GeoLite2-City')
    # first check if current file is up to date
    # creation file name format is 'create_YYYYMMDD'
    date = [f for f in os.listdir(geo_ip_db_folder) if f.startswith('created')].pop()[-8:]
    month = int(date[4:6])
    if True or ((datetime.today().month - month) % 12) > 1:
        # if not download the new version

        # if that succeeds delete the old one

        # replace with new one and update file paths
        base_name = 'GeoLite2-City.tar.gz'
        # geo_url = 'https://geolite.maxmind.com/download/geoip/database/' + base_name
        tmp_tar_gz = '/tmp/' + base_name
        # with urllib.request.urlopen(geo_url) as f_in:
        #     with open(tmp_tar_gz, 'wb') as f_out:
        #         shutil.copyfileobj(f_in, f_out)

        with tarfile.open(tmp_tar_gz, "r:gz") as tar:
            tar.extractall('/tmp/geo_ip/')

        return "Geo-location database has been updated."
    return "Geo-location database is fairly current."

