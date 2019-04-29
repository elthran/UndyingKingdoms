from flask import jsonify, request
from flask.views import MethodView
from flask_login import login_required, current_user

from tests import bp
from undyingkingdoms.api.vue_safe import vue_safe_form, generic_vue_safe
from undyingkingdoms.models import Technology
from undyingkingdoms.models.forms.technology import TechnologyForm


class UpdateAPI(MethodView):
    @login_required
    def get(self):
        county = current_user.county

        known_technologies = [
            generic_vue_safe(tech, ['name', 'description'])
            for tech in county.completed_techs
        ]
        all_technologies = [
            generic_vue_safe(tech, ['name', 'description', 'tier'])
            for tech in county.technologies.values()
        ]

        form = TechnologyForm()
        form.technology.choices = [
            (tech.id, tech.name)
            for tech in county.available_techs
        ]

        county_data = dict(
            research=county.research,
        )

        current_tech = county.research_choice
        return jsonify(
            debugMessage=f"You called on {__name__}",
            form=vue_safe_form(form),
            county=county_data,
            knownTechnologies=known_technologies,
            allTechnologies=all_technologies,
            researchChange=county.get_research_change(),
            currentTech=current_tech.name,
            description=current_tech.description,
            selectedResearch=current_tech.id,
            progressCurrent=current_tech.current,
            progressRequired=current_tech.cost,
        )

    @login_required
    def post(self):
        county = current_user.county
        form = TechnologyForm()

        form.technology.choices = [
            (tech.id, tech.name)
            for tech in county.available_techs
        ]

        if form.validate_on_submit():
            tech = Technology.query.get(form.technology.data)
            # update choice.
            county.research_choice = tech

            bp()
            return jsonify(
                debugMessage='You have updated your current research choice.',
                researchChange=county.get_research_change(),
                description=tech.description,
                progressCurrent=tech.current,
                progressRequired=tech.cost,
                form=vue_safe_form(form)
            ), 201
        return jsonify(
            debugMessage='Your research form did not pass validation.'
        ), 403
