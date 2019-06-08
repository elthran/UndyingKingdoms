from flask import jsonify
from flask.views import MethodView
from flask_login import login_required, current_user

from undyingkingdoms.api.vue_safe import vue_safe_form, generic_vue_safe
from undyingkingdoms.models.exports import Technology
from undyingkingdoms.models.forms.technology import TechnologyForm


class UpdateAPI(MethodView):
    @login_required
    def get(self):
        county = current_user.county

        known_technologies = [
            generic_vue_safe(tech, ['name', 'description', 'source'])
            for tech in county.completed_technologies
        ]
        available_technologies = [
            generic_vue_safe(tech, ['name', 'description', 'tier', 'current', 'cost', 'source'])
            for tech in county.available_technologies
        ]

        locked_technologies = [
            generic_vue_safe(tech, ['name', 'description', 'tier', 'current', 'cost', 'source'])
            for tech in county.unavailable_technologies
        ]

        form = TechnologyForm()
        form.technology.choices = [
            (tech.id, tech.name)
            for tech in county.available_technologies
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
            availableTechnologies=available_technologies,
            researchChange=county.research_change,
            currentTech=current_tech.name,
            description=current_tech.description,
            selectedResearch=current_tech.id,
            progressCurrent=current_tech.current,
            progressRequired=current_tech.cost,
            lockedTechnologies=locked_technologies,
        )

    @login_required
    def post(self):
        county = current_user.county
        form = TechnologyForm()

        form.technology.choices = [
            (tech.id, tech.name)
            for tech in county.available_technologies
        ]

        if form.validate_on_submit():
            tech = Technology.query.get(form.technology.data)
            # update choice.
            county.research_choice = tech
            return jsonify(
                debugMessage='You have updated your current research choice.',
                researchChange=county.research_change,
                description=tech.description,
                progressCurrent=tech.current,
                progressRequired=tech.cost,
                form=vue_safe_form(form)
            ), 201
        return jsonify(
            debugMessage='Your research form did not pass validation.'
        ), 403
