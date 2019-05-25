import hashlib
import subprocess
from random import randint

from flask import render_template
from flask_login import current_user
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

import private_config
from undyingkingdoms import app, User

error_log_cache = {}


@app.errorhandler(404)
def not_found(error):
    print("Error:", error)
    return render_template('404.html', error=error), 404


@app.errorhandler(500)
def server_fault(error, admin_id=None):
    error_log = get_error_log()

    # TODO hash error log an only send once per error!
    # log_hash = hashlib.md5(error_log)
    # if log_hash not in error_log_cache:
    #     error_log_cache[log_hash] = error_log


    try:
        county = current_user.county
        county_name = county.name
    except AttributeError:
        county = None
        county_name = None

    if current_user.is_authenticated:
        user_name = current_user.username
        user_email = current_user.email
        user_info = f'{user_name} <{user_email}>'
    else:
        user_info = "AnonymousUser"

    admin_id_to_message = admin_id or randint(1, 2)
    admin = User.query.get(admin_id_to_message)
    admin_name = admin.username
    admin_email = admin.email
    county_info = f' of {county_name} county' if county and county_name else ''

    from_email = "Undying Kingdoms <no-reply@undyingkingdoms.com>"
    subject = 'The server is crashing!!!'
    to_email = f"Admin '{admin_name}' <{admin_email}>"
    content = render_template(
        'email/error_body.html',
        admin_name=admin_name,
        error=error,
        user_info=user_info,
        county_info=county_info,
        error_log=error_log,
    )

    message = Mail(
        from_email=from_email,
        to_emails=to_email,
        subject=subject,
        plain_text_content=content
    )

    try:
        sg = SendGridAPIClient(api_key=private_config.SENDGRID_API_KEY)
        # noinspection PyUnresolvedReferences
        response = sg.send(message)
        assert response.status_code == 202
    except Exception as e:
        print("Error: ", e)
        print("While trying to send message:")
        print(message)
        print("Status code was: ", response.status_code)
    return render_template('500.html', error=error, admin=admin_name), 500


def get_error_log():
    # If this code is slow update it.
    log_file = "/var/log/www.undyingkingdoms.com.error.log"
    error_log = ""
    f = subprocess.Popen(['tail', '-n100', log_file], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    for line in f.stdout.readlines():
        error_log += line.decode('utf-8').replace('\n', "<br>")
    return error_log
