import os

#from maxminddb import open_database
from flask import Blueprint, request, current_app, jsonify

# causes import loop, need to refactor model design
# from app.models.exports import User

geo_ip = Blueprint('geoip', __name__, url_prefix='/geo_ip')


def touch(path):
    """Create file at location with current timestamps."""
    with open(path, 'w'):
        os.utime(path, None)


@geo_ip.route('/check')
def check_ip_against_geo_db():
    """Check your IP address for location data.

    Options: /check?ip=... (an ip address)
    """
    geo_ip_db = 'GeoLite2-City/GeoLite2-City.mmdb'
    geo_ip_db_path = os.path.join(current_app.static_folder, geo_ip_db)

    arg_ip = request.args.get('ip')
    ip = arg_ip if arg_ip else request.access_route[0]

    info = {
        "Remote IP": ip,
        "Access route": 'Request via /check?ip=...' if arg_ip else request.access_route
    }
    with open_database(geo_ip_db_path) as reader:
        data = reader.get(ip)
        try:
            info["Country"] = data['country']['iso_code']
            info["Subdivision"] = [division['names']['en'] for division in data['subdivisions']][0]
            info["City"] = data['city']['names']['en']
            # Store in User object?
        except TypeError:
            info["Location"] = "Not Found"
    return jsonify(info)


@geo_ip.route('/update')
def update_geo_ip_database():
    """Update the current IP geo-location database.

    Options: /update?force=true (an ip address)

    Note: I'm not sure if my code is bugged or if the current
    downloadable database is.
    """
    import urllib.request
    import shutil
    import tarfile
    from datetime import datetime

    force = request.args.get('force') == 'true'

    geo_ip_db_folder = os.path.join(current_app.static_folder, 'GeoLite2-City')

    # creation file name format is 'create_YYYYMMDD'
    try:
        date = [f for f in os.listdir(geo_ip_db_folder) if f.startswith('created')].pop()[-8:]
        month = int(date[4:6])
    except FileNotFoundError:
        # force update
        date = 'bugged_backup'
        month = datetime.today().month - 2
    # first check if current file is up to date
    if force or ((datetime.today().month - month) % 12) > 1:
        # file is not up to date so download the new version
        base_name = 'GeoLite2-City.tar.gz'
        geo_url = 'https://geolite.maxmind.com/download/geoip/database/' + base_name
        tmp_tar_gz = '/tmp/' + base_name
        try:
            # Download the file from `url` and save it locally under `file_name`:
            with urllib.request.urlopen(geo_url) as response, open(tmp_tar_gz, 'wb') as out_file:
                shutil.copyfileobj(response, out_file)
        except Exception as ex:
            return str(ex)

        # if that succeeds, backup the old one
        try:
            shutil.copytree(geo_ip_db_folder, geo_ip_db_folder + "_" + date)
        except FileNotFoundError:
            pass
        except FileExistsError:
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
        try:
            shutil.copytree('/tmp/geo_ip/' + folder, geo_ip_db_folder)
        except FileExistsError:
            pass

        # create timestamp file
        touch(geo_ip_db_folder + '/created_' + date_str)

        return "Geo-location database has been updated."
    return "Geo-location database is fairly current, come back in a month or so."
