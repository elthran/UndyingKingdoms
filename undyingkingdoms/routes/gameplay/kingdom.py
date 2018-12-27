from flask import render_template, url_for, redirect
from flask_login import login_required, current_user

from undyingkingdoms import app, db
from undyingkingdoms.models import Kingdom, World
from undyingkingdoms.models.forms.votes import VoteForm


@app.route('/gameplay/kingdom/<int:kingdom_id>/', methods=['GET', 'POST'])
@login_required
def kingdom(kingdom_id=0):
    if not current_user.logged_in:
        current_user.logged_in = True
    kingdom = Kingdom.query.filter_by(id=kingdom_id).first()

    # Random testing
    world = World.query.first()
    world. reset_age()

    form = VoteForm(vote=current_user.county.vote)
    form.vote.choices = [(county.id, county.name) for county in current_user.county.kingdom.counties]
    if form.validate_on_submit():
        current_user.county.cast_vote(form.vote.data)
        db.session.commit()
        return redirect(url_for('kingdom', kingdom_id=kingdom.id))
    return render_template('gameplay/kingdom.html', form=form, kingdom=kingdom)
