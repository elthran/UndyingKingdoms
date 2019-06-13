from flask import jsonify
from flask.views import MethodView
from flask_login import login_required, current_user

from .helpers import build_units, max_trainable_by_cost, monsters_buildable
from undyingkingdoms.metadata.metadata import game_descriptions
from undyingkingdoms.models.forms.military import MilitaryForm
from undyingkingdoms.api.vue_safe import vue_safe_form, generic_vue_safe


class UpdateAPI(MethodView):
    @login_required
    def get(self):
        county = current_user.county
        form = MilitaryForm()
        form.county_id.data = county.id

        return jsonify(
            debugMessage=f"You called on {__name__}",
            form=vue_safe_form(form),
            meta_data=game_descriptions,
            # max_trainable_by_cost=max_trainable_by_cost,
            # monsters_buildable=monsters_buildable
        )

    @login_required
    def post(self):
        county = current_user.county
        form = MilitaryForm()

        if form.validate_on_submit():
            build_units(county, form)
            return jsonify(
                debugMessage='You have updated your current troop production.',
            ), 201
        return jsonify(
            debugMessage='Your troop production form did not pass validation.'
        ), 403
