from flask import jsonify, render_template
from markdown import markdown
from markupsafe import Markup

from lib.mail import send_email, SUCCESS
from undyingkingdoms.models.exports import User


def email_newsletter():
    from_email = "Undying Kingdoms <no-reply@undyingkingdoms.com>"
    subject = 'Newsletter'

    # TODO: write newsletter in Markdown
    with open('newsletter.md') as f:
        content = Markup(markdown(f.read()))

    all_users = User.query.all()
    sent_to_addresses = []

    for user in all_users[:1]:  # during testing only use the first user.
        user_name = user.username
        user_email = user.email

        to_email = f"'{user_name}' <{user_email}>"
        content = render_template(
            'email/newsletter_body.html',
            user_name=user_name,
            content=content
        )

        status = send_email(content, from_email, subject, to_email)
        if status == SUCCESS:
            sent_to_addresses.append(user_email)

    return jsonify(
        status="success",
        message=f"Sent newsletter to: '{sent_to_addresses!r}'."
    )
