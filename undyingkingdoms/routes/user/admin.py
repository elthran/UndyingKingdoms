from random import randint, choice
from uuid import uuid4

from flask import render_template, request
from flask_login import login_required, current_user
from flask_wtf import FlaskForm
from wtforms import SubmitField

from undyingkingdoms import app, db
from undyingkingdoms.models.kingdoms import Kingdom
from undyingkingdoms.models.counties import County
from undyingkingdoms.models.users import User


class AdminForm(FlaskForm):
    submit = SubmitField('Do this')


bot_county_prefix = ["Eldritch", "Dengmar", "Zort", "Pralde", "Eggroth", "Wuanlo"]
bot_county_suffix = ["ville", " Town", "ion", "oth", " Land"]

bot_leader_prefix = ["Skri", "Aldar", "Frel", "Eldr", "Toth", "Zon", "Pandish", "Gresk", "Linsk"]
bot_leader_suffix = ["oth", "ith", "ion", "ilisk", "anth", "ills", "ondo", "alasl"]


@login_required
@app.route('/user/admin/', methods=['GET', 'POST'])
def admin():
    if not current_user.in_active_session:
        current_user.in_active_session = True
    bot_form = AdminForm()
    kingdoms = Kingdom.query.all()
    if bot_form.validate_on_submit():
        for i in range(3):
            smallest_kingdom = min(kingdoms, key=lambda x: len(x.counties))
            for kingdom in kingdoms:
                if kingdom.counties is None:
                    smallest_kingdom = kingdom
            bot_name = uuid4()
            user = User("bot_{}".format(bot_name), "bot_{}@gmail.com".format(bot_name), "1234")
            user.is_bot = True
            user.save()
            county = County(smallest_kingdom.id, "{}{}".format(choice(bot_county_prefix), choice(bot_county_suffix)),
                            "{}{}".format(choice(bot_leader_prefix), choice(bot_leader_suffix)), user.id,
                            choice(["Human", "Elf", "Dwarf"]), choice(["Male", "Female"]),
                            choice(["Engineer", "Warlord", "Rogue", "Merchant"]))
            county.save()
            county.vote = county.id
    return render_template('user/admin.html', form=bot_form)
