from python_http_client import UnauthorizedError
from sendgrid import Mail, SendGridAPIClient

import private_config

FAIL = 0
SUCCESS = 1


def send_email(content, from_email, subject, to_email):
    message = Mail(
        from_email=from_email,
        to_emails=to_email,
        subject=subject,
        html_content=content
    )
    sg = SendGridAPIClient(api_key=private_config.SENDGRID_API_KEY)
    try:
        # noinspection PyUnresolvedReferences
        response = sg.send(message)
    except UnauthorizedError as ex:
        response = None
        print("Email error: ", ex)

    if response is None:
        print(f"While trying to send message to {to_email!r}")
        return FAIL
    elif response.status_code != 202:
        print(f"While trying to send message to {to_email!r}")
        print("Status code was: ", response.status_code)
        return FAIL

    return SUCCESS
