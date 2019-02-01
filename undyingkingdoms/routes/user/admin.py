from uuid import uuid4

from flask import render_template, request
from flask_login import login_required, current_user

from undyingkingdoms import app, db
from undyingkingdoms.models.users import User


@login_required
@app.route('/user/admin/', methods=['GET', 'POST'])
def achievements():
    if not current_user.in_active_session:
        current_user.in_active_session = True
    if request.form['generate_ai'] == 'Create 3 Bot Accounts':
        for i in range(3):
            bot_name = uuid4()
            user = User("bot_{}".format(bot_name), "bot_{}@gmail.com".format(bot_name), "1234")
            user.is_bot = True
            user.save()
    return render_template('user/admin.html')
