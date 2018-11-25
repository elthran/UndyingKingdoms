from flask import render_template, url_for, redirect
from flask_login import login_required, current_user

from undyingkingdoms import app, db
from undyingkingdoms.models import Kingdom
from undyingkingdoms.models.forms.votes import VoteForm


@login_required
@app.route('/gameplay/kingdom/<int:kingdom_id>/', methods=['GET', 'POST'])
def kingdom(kingdom_id=0):
    kingdom = Kingdom.query.filter_by(id=kingdom_id).first()
    form = VoteForm(vote=current_user.county.vote)
    form.vote.choices = [(county.id, county.name) for county in current_user.county.kingdom.counties]
    if form.validate_on_submit():
        current_user.county.cast_vote(form.vote.data)
        db.session.commit()
        return redirect(url_for('kingdom'))
    return render_template('gameplay/kingdom.html', form=form, kingdom=kingdom)
