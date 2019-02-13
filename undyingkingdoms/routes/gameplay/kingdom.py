from flask import render_template, url_for, redirect
from flask_login import login_required, current_user
from flask_mobility.decorators import mobile_template

from undyingkingdoms import app
from undyingkingdoms.models import Kingdom
from undyingkingdoms.models.forms.votes import VoteForm
from undyingkingdoms.routes.helpers import in_active_session


@app.route('/gameplay/kingdom/<int:kingdom_id>/', methods=['GET', 'POST'])
@mobile_template('{mobile/}gameplay/kingdom.html')
@login_required
@in_active_session
def kingdom(template, kingdom_id=0):
    kingdom = Kingdom.query.filter_by(id=kingdom_id).first()
    form = VoteForm(vote=current_user.county.vote)
    form.vote.choices = [(county.id, county.name) for county in current_user.county.kingdom.counties]
    if form.validate_on_submit():
        current_user.county.cast_vote(form.vote.data)
        return redirect(url_for('kingdom', kingdom_id=kingdom.id))
    return render_template(template, form=form, kingdom=kingdom)
