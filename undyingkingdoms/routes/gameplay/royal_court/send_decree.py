from flask import url_for, jsonify
from flask_login import login_required, current_user
from werkzeug.utils import redirect

from undyingkingdoms import app
from undyingkingdoms.models import County, Notification
from undyingkingdoms.models.forms.royal_court import RoyalCourtMessageForm


@app.route('/gameplay/send_decree/', methods=['POST'])
@login_required
def send_decree():
    county = current_user.county
    if county.id != county.kingdom.leader:
        return redirect(url_for('overview'))
    message_form = RoyalCourtMessageForm()
    if message_form.validate_on_submit():
        for county in County.query.filter_by(kingdom_id=county.kingdom_id).all():
            message = Notification(
                county_id=county.id,
                title=f"Royal Decree from {county.title} {county.leader}",
                content=message_form.content.data,
                day=county.kingdom.world.day,
                category="Royal Decree")
            message.save()
        return redirect(url_for('royal_court'))
    return jsonify(
        status='fail',
        message="Your message didn't pass form validation.")
