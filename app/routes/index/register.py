from importlib import import_module

from flask import url_for, redirect, render_template
from flask_login import current_user
from flask_login import login_user
from flask_mobility.decorators import mobile_template
from app import app
from app.models.tutorial import Tutorial

get_models = lambda: import_module('app.models.exports')
get_forms = lambda: import_module('app.models.forms.register')


@app.route('/register/', methods=['GET', 'POST'])
@mobile_template('{mobile/}index/register.html')
def register(template):
    forms = get_forms()
    models = get_models()
    form = forms.RegisterForm()
    if current_user.is_authenticated:
        return redirect(url_for('overview'))

    if form.validate_on_submit():
        user = models.User(form.username.data, form.email.data, form.password.data)
        user.save()
        tutorial = Tutorial(user.id, "ftue", "Economics", 4)
        tutorial.save()
        login_user(user)
        return redirect(url_for('initialize'))
    return render_template(template, form=form)
