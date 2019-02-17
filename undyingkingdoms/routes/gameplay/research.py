from flask import render_template
from flask_login import login_required, current_user
from flask_mobility.decorators import mobile_template

from undyingkingdoms import app
from undyingkingdoms.models.forms.technology import TechnologyForm
from undyingkingdoms.models.technologies import Technology


@app.route('/gameplay/research/', methods=['GET'])
@mobile_template("{mobile/}gameplay/research.html")
@login_required
def research(template):
    county = current_user.county
    form = TechnologyForm()

    available_technologies = Technology.query.filter_by(county_id=county.id).filter_by(completed=False).all()
    form.technology.choices = [(i, available_technologies[i].name) for i in range(len(available_technologies))]

    return render_template(template, form=form, available_technologies=available_technologies)
