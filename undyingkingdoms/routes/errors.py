import subprocess
from random import randint

from flask import render_template
from flask_login import current_user
from sendgrid import SendGridAPIClient

import private_config
from undyingkingdoms import app, User


@app.errorhandler(404)
def not_found(error):
    print("Error:", error)
    return render_template('404.html', error=error), 404


@app.errorhandler(500)
def server_fault(error):
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

    admin_id_to_message = randint(1, 2)
    admin = User.query.get(admin_id_to_message)
    admin_name = admin.username
    admin_email = admin.email

    # If this code is slow update it.
    log_file = "/var/log/www.undyingkingdoms.com.error.log"
    error_log = ""
    f = subprocess.Popen(['tail', '-n100', log_file], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    for line in f.stdout.readlines():
        error_log += line.decode('utf-8').replace('\n', "<br />")

    county_info = f' of {county_name} county' if county and county_name else ''

    from_email = "Undying Kingdoms <no-reply@undyingkingdoms.com>"
    subject = 'The server is crashing!!!'
    to_email = f"Admin '{admin_name}' <{admin_email}>"
    content = f"""<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
        <html xmlns="http://www.w3.org/1999/xhtml">
         <head>
          <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
          <title>Reset Password Email</title>
          <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
        </head>
        <body style="margin: 0; padding: 0;">
         <table border="0" cellpadding="0" cellspacing="0" width="100%">
          <tr>
           <td>.user
            <p>Hi Admin '{admin_name}',</p>
            <p>The server is currently crashing with error: {error}</p>
            <p>This error was found/caused by {user_info}{county_info},
                you should probably thank them for bringing this to our attention.
            <p>The debug log is as follows.</p>
            <p>{error_log}</p>
           </td>
          </tr>
         </table>
        </body>
        </html>
        """

    data = {
        "personalizations": [
            {
                "to": [
                    {
                        "email": to_email
                    }
                ],
                "subject": subject
            }
        ],
        "from": {
            "email": from_email
        },
        "content": [
            {
                "type": "text/html",
                "value": content
            }
        ]
    }

    try:
        sg = SendGridAPIClient(api_key=private_config.SENDGRID_API_KEY)
        # noinspection PyUnresolvedReferences
        sg.send(data)
    except Exception as e:
        print(e, data)
    return render_template('500.html', error=error, admin=admin_name), 500
