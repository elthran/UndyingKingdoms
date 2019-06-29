from flask import jsonify
from flask_login import current_user

from undyingkingdoms.models.counties.counties import County
from undyingkingdoms.models.notifications import Notification


def create_notification(message):
    for county in County.query.all():
        notification = Notification(
            county,
            f"Admin Update from {current_user.county.leader}",
            message,
            "Admin"
        )
        notification.save()
    return jsonify(
        status="success",
        message=f"Successfully sent notice '{message}' to all active users."
    )
