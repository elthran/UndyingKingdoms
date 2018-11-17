from flask import render_template, url_for, redirect
from flask_login import login_required, current_user

from undyingkingdoms import app, db
from undyingkingdoms.models.forms.votes import VoteForm


@login_required
@app.route('/gameplay/kingdom/', methods=['GET', 'POST'])
def kingdom():
    form = VoteForm(vote=current_user.county.vote)
    form.vote.choices = [(county.id, county.name) for county in current_user.county.kingdom.counties]
    if form.validate_on_submit():
        current_user.county.cast_vote(form.vote.data)
        db.session.commit()
        return redirect(url_for('kingdom'))
    return render_template('gameplay/kingdom.html', form=form)
