from flask import render_template, jsonify, request
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
    known_technologies = Technology.query.filter_by(county_id=county.id).filter_by(completed=True).all()
    form.technology.choices = [(tech.id, tech.name) for tech in available_technologies]

    current_tech = Technology.query.filter_by(county_id=county.id, name=county.research_choice).first()

    return render_template(
        template,
        form=form,
        available_technologies=available_technologies,
        known_technologies=known_technologies,
        research_change=county.get_research_change(),
        current_tech=current_tech
    )


@app.route('/gameplay/research/api', methods=['POST'])
def research_api():
    """This route"""
    county = current_user.county
    form = TechnologyForm()

    available_technologies = Technology.query.filter_by(county_id=county.id).filter_by(completed=False).all()
    form.technology.choices = [(tech.id, tech.name) for tech in available_technologies]

    if form.validate_on_submit():
        tech = Technology.query.get(form.technology.data)
        # update choice.
        county.research_choice = tech.name

        return jsonify(
            status='success',
            message='You have updated your current research choice.',
            researchChange=county.get_research_change(),
            description=tech.description,
            progressCurrent=tech.current,
            progressRequired=tech.required,
        )
    return jsonify(
        status='fail',
        message='Your research form did not pass validation.'
    )
