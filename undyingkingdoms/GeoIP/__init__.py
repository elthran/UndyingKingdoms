import os

import maxminddb
from flask import Blueprint, request, current_app, jsonify

# causes import loop, need to refactor model design
# from undyingkingdoms.models.users import User

geo_ip = Blueprint('geoip', __name__, url_prefix='/geo_ip')


def touch(path):
    """Create file at location with current timestamps."""
    with open(path, 'w'):
        os.utime(path, None)


@geo_ip.route('/pull_ip')
def pull_ip():
    # import pdb;pdb.set_trace()
    geo_ip_db = 'GeoLite2-City/GeoLite2-City.mmdb'
    geo_ip_db_path = os.path.join(current_app.static_folder, geo_ip_db)
    # optionally
    info = {
        "Remote IP": request.remote_addr,
        "Access route": request.access_route
    }

    ip = request.access_route[0]
    with maxminddb.open_database(geo_ip_db_path) as reader:
        data = reader.get(ip)
        try:
            info["Country"] = data['country']['iso_code']
            info["Subdivisions"] = [division['names']['en'] for division in data['subdivisions']]
            info["City"] = data['city']['names']['en']
            # Store in User object?
        except TypeError:
            info["Location"] = "Not Found"
    return jsonify(info)


@geo_ip.route('/update')
def update_geo_ip_database():
    import urllib.request
    import shutil
    import tarfile
    from datetime import datetime

    geo_ip_db_folder = os.path.join(current_app.static_folder, 'GeoLite2-City')

    # creation file name format is 'create_YYYYMMDD'
    date = [f for f in os.listdir(geo_ip_db_folder) if f.startswith('created')].pop()[-8:]
    month = int(date[4:6])
    # first check if current file is up to date
    if ((datetime.today().month - month) % 12) > 1:
        # file is not up to date so download the new version
        base_name = 'GeoLite2-City.tar.gz'
        geo_url = 'https://geolite.maxmind.com/download/geoip/database/' + base_name
        tmp_tar_gz = '/tmp/' + base_name
        try:
            with urllib.request.urlopen(geo_url) as f_in:
                with open(tmp_tar_gz, 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)
        except Exception as ex:
            return str(ex)

        # if that succeeds delete the old one
        try:
            shutil.rmtree(geo_ip_db_folder)
        except FileNotFoundError:
            pass

        # Next extract and replace old data with new data.
        try:
            with tarfile.open(tmp_tar_gz, "r:gz") as tar:
                tar.extractall('/tmp/geo_ip/')
                os.remove(tmp_tar_gz)
        except FileNotFoundError:
            pass

        timestamped_folder = [f for f in os.listdir('/tmp/geo_ip/')].pop()
        folder, date_str = timestamped_folder.split('_')
        try:
            shutil.copytree('/tmp/geo_ip/' + timestamped_folder, '/tmp/geo_ip/' + folder)
        except FileExistsError:
            pass
        shutil.move('/tmp/geo_ip/' + folder, current_app.static_folder)

        # create timestamp file
        touch(geo_ip_db_folder + '/created_' + date_str)

        return "Geo-location database has been updated."
    return "Geo-location database is fairly current, come back in a month or so."
