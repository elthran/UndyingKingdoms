from flask import render_template, url_for, redirect
from flask_login import login_required, current_user
from flask_mobility.decorators import mobile_template

from undyingkingdoms import app
from undyingkingdoms.models.counties.counties import County
from undyingkingdoms.models.exports import Kingdom
from undyingkingdoms.models.forms.votes import VoteForm


def kingdom_navigation(direction, current_id):
    all_kingdoms = Kingdom.query.all()
    eligible_kingdoms = [kingdom for kingdom in all_kingdoms if len(kingdom.counties) > 0]
    eligible_kingdoms = sorted(eligible_kingdoms, key=lambda x: x.id)
    currently_viewing = Kingdom.query.get(current_id)
    current_index = eligible_kingdoms.index(currently_viewing)
    if len(eligible_kingdoms) == 1:
        return eligible_kingdoms[0].id
    if direction == 'left':
        if current_index == 0:
            return eligible_kingdoms[-1].id
        return eligible_kingdoms[current_index - 1].id
    elif direction == 'right':
        if current_index == len(eligible_kingdoms) - 1:
            return eligible_kingdoms[0].id
        return eligible_kingdoms[current_index + 1].id


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
    return render_template(
        template,
        form=form,
        kingdom=kingdom,
        kingdom_navigation=kingdom_navigation
    )
