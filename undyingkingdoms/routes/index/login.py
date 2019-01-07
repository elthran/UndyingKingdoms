from flask import url_for, redirect, render_template, flash, jsonify
from flask.views import MethodView
from flask_login import current_user
from flask_login import login_user

from undyingkingdoms import app, User
from undyingkingdoms.models.forms.login import LoginForm


@app.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if current_user.is_authenticated:
        return redirect(url_for('overview', kingdom_id=current_user.county.kingdom.id, county_id=current_user.county.id))
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            if current_user.county is None:
                return redirect(url_for('initialize'))
            return redirect(url_for('overview', kingdom_id=current_user.county.kingdom.id, county_id=current_user.county.id))
        else:
            flash("Your email or password was incorrect.")
    return render_template("index/login.html", form=form)


class LoginAPI(MethodView):
    def post(self):
        form = LoginForm()
        if current_user.is_authenticated:
            return jsonify(
                status='success',
                message='User is already logged in. Redirect to overview page.',
                redirect=url_for(
                    'overview',
                    kingdom_id=current_user.county.kingdom.id,
                    county_id=current_user.county.id
                )
            ), 200
        elif form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user and user.check_password(form.password.data):
                login_user(user)
                if current_user.county is None:
                    return jsonify(
                        status='success',
                        message='User is authenticated. Account has been reset. Redirect to initialize page.',
                        redirect=url_for('initialize')
                    ), 200
                else:
                    return jsonify(
                        status='success',
                        message='User has been logged in. Redirect to overview page.',
                        redirect=url_for(
                            'overview',
                            kingdom_id=current_user.county.kingdom.id,
                            county_id=current_user.county.id
                        )
                    ), 200
            elif user:
                return jsonify(
                    status='fail',
                    message='Your email or password was incorrect.'
                ), 200
            else:
                return jsonify(
                    status='fail',
                    message='The requested user does not exist.'
                ), 200
        else:
            return jsonify(
                status='fail',
                message='The data sent is not in an acceptable form.'
            ), 200


app.add_url_rule('/login', view_func=LoginAPI.as_view('login_api'))
