from flask import url_for, redirect, render_template
from flask_login import current_user
from sendgrid import SendGridAPIClient

import private_config
from undyingkingdoms import app
from undyingkingdoms.models.forms.activate import EmailVerificationForm


@app.route('/activate/', methods=['GET', 'POST'])
def activate():
    form = EmailVerificationForm()
    user = current_user
    #TODO: make this only send once unless user request resend.
    #TODO: hash should be different every time.
    email_hash = user.generate_verification_hash()

    from_email = "Undying Kingdoms <no-reply@undyingkingdoms.com>"
    subject = 'Welcome to Undying Kingdoms'
    to_email = f"Owner of account '{user.username}' <{user.email}>"
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
       <td>
        <p>Hi Owner of account '{user.username}',</p>
        <p>&#9;You\'ll need this code to activate your account: <strong id="key">{email_hash}</strong>
        </p>
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
        response = sg.send(data)
        # print(user.email)
        # print(response.status_code)
        # print(response.body)
        # print(response.headers)
    except Exception as e:
        print(e, data)

    if form.validate_on_submit():
        if user.verify_verification_hash(form.code.data):
            user.is_verified = True
            return redirect(url_for('initialize'))
    return render_template(
        'index/activate.html',
        form=form,
        user=user
    )
