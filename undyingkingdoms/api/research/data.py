from flask import jsonify, request
from flask.views import MethodView
from flask_login import login_required, current_user

from undyingkingdoms.api.vue_safe import vue_safe_form
from undyingkingdoms.models import Technology
from undyingkingdoms.models.forms.technology import TechnologyForm


class DataAPI(MethodView):
    @login_required
    def get(self):
        county = current_user.county


        available_technologies = list(county.available_techs)
        known_technologies = county.completed_techs
        all_technologies = county.technologies.values()

        form = TechnologyForm()
        form.technology.choices = [(tech.id, tech.name.title()) for tech in available_technologies]

        county_data = dict(
            research=county.research,
        )
        return jsonify(
            debugMessage=f"You called on {__name__}",
            form=vue_safe_form(form),
            # availableTechnologies=available_technologies,
            # knownTechnologies=known_technologies,
            # allTechnologies=all_technologies,
            researchChange=county.get_research_change(),
            currentTech=county.research_choice
        )
