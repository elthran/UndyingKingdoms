from flask import render_template
from flask_login import login_required, current_user

from undyingkingdoms import app, db
from undyingkingdoms.models import County, World


@app.route('/gameplay/testing_page/', methods=['GET', 'POST'])
@login_required
def testing_page():
    if not current_user.logged_in:
        current_user.logged_in = True
    # Random testing
    world = World.query.first()
    world.reset_age()
    current_test_message = "Using this page to test age resets."
    return current_test_message
