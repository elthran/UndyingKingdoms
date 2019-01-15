from flask import render_template
from flask_login import login_required, current_user

from undyingkingdoms import app
from undyingkingdoms.models import World
from undyingkingdoms.models.forms.attack import TempGameAdvance


@app.route('/gameplay/testing_page/', methods=['GET', 'POST'])
@login_required
def testing_page():
    if not current_user.logged_in:
        current_user.logged_in = True
    # Below is clock functions
    world = World.query.first()
    form = TempGameAdvance()
    if form.validate_on_submit():
        world.advance_day()
        world.advance_24h_analytics()
    # End of clock functions
    return render_template('gameplay/test_page.html', form=form)
