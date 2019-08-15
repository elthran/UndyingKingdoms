from flask import request, jsonify
from flask_login import login_required, current_user
from werkzeug.utils import redirect

from app import app


@app.route('/gameplay/generic/click_next_tutorial_step/<string:tutorial_name>/<int:current_step>', methods=['GET', 'POST'])
@login_required
def click_next_tutorial_step(tutorial_name, current_step):
    """
    Make sure the url is only passing in a current tutorial and that the current step can be skipped.
    """

    user = current_user
    tutorial = None
    for each_tutorial in user.tutorials:
        if each_tutorial.name == tutorial_name:
            tutorial = each_tutorial
            break
    if tutorial:
        if tutorial.current_step == current_step and tutorial.is_clickable_step():
            tutorial.advance_step(current_step)

    path = request.headers["Referer"].rsplit('/', maxsplit=1)[0]
    return redirect(f"{path}/{tutorial.current_step}")


@app.route("/gameplay/tutorial/current")
@login_required
def tutorial_current():
    tutorial = current_user.tutorials[0]
    return jsonify(
        tutorial=tutorial
    )
