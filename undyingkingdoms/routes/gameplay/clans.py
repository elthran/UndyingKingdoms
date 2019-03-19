from flask import render_template, redirect, url_for, jsonify, request, send_from_directory, current_app
from flask_login import login_required, current_user
from flask_mobility.decorators import mobile_template

from undyingkingdoms import app
from undyingkingdoms.models.forms.create_kingdom import CreateKingdomForm
from undyingkingdoms.models.forms.economy import EconomyForm
from undyingkingdoms.static.metadata.metadata import rations_terminology, birth_rate_modifier, income_modifier, \
    food_consumed_modifier, happiness_modifier


@app.route('/gameplay/clans/', methods=['GET'])
@mobile_template('{mobile/}gameplay/clans.html')
@login_required
def clans(template):
    form = CreateKingdomForm()


    return render_template(
        template,
        form=form)


@app.route('/gameplay/clans_create/', methods=['GET', 'POST'])
@login_required
def clans_create(template):

    return render_template(
        template)
