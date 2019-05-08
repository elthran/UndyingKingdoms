from flask import render_template, url_for, redirect
from flask_login import login_required, current_user
from flask_mobility.decorators import mobile_template

from undyingkingdoms import app
from undyingkingdoms.models.counties.counties import County
from undyingkingdoms.models.exports import Kingdom
from undyingkingdoms.models.forms.votes import VoteForm


@app.route('/gameplay/kingdom/<int:kingdom_id>/', methods=['GET', 'POST'])
@mobile_template('{mobile/}gameplay/kingdom.html')
@login_required
def kingdom(template, kingdom_id=0):
    county = current_user.county
    preferences = county.preferences
    kingdom = Kingdom.query.get(kingdom_id)

    form = VoteForm(vote=preferences.vote_id)
    form.vote.choices = [(county.id, county.name) for county in county.kingdom.counties]
    if form.validate_on_submit():
        vote = County.query.get(form.vote.data)
        county.cast_vote(vote)
        return redirect(url_for('kingdom', kingdom_id=kingdom.id))
    return render_template(template, form=form, kingdom=kingdom)
