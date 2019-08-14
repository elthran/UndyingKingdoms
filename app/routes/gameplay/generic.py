from datetime import time
from importlib import import_module

from math import floor
from random import randint

from flask import request
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
        if tutorial.current_step == current_step and tutorial.get_step_description(get_click=True):
            tutorial.advance_step(current_step)
            
    return redirect(request.url)

