from flask import render_template, url_for, redirect
from flask_login import login_required, current_user

from undyingkingdoms import app, db
from undyingkingdoms.models import World
from undyingkingdoms.models.forms.attack import TempGameAdvance


@login_required
@app.route('/gameplay/overview/', methods=['GET', 'POST'])
def overview():
    if not current_user.county:
        return redirect(url_for('initialize'))

    # Below is clock functions
    world = World.query.first()
    world.check_clock()
    form = TempGameAdvance()
    if form.validate_on_submit():
        world.advance_day()
    # End of clock functions
    return render_template('gameplay/overview.html', form=form)
