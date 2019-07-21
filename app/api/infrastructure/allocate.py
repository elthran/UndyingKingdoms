from importlib import import_module

from flask import jsonify
from flask.views import MethodView
from flask_login import login_required, current_user

get_forms = lambda: import_module('app.models.forms.infrastructure')
from app.metadata.metadata import excess_worker_choices


class AllocateAPI(MethodView):
    @login_required
    def post(self):
        forms = get_forms()
        county = current_user.county
        excess_worker_form = forms.ExcessProductionForm(goal=county.production_choice)
        excess_worker_form.goal.choices = excess_worker_choices

        if excess_worker_form.validate_on_submit():
            county.production_choice = excess_worker_form.goal.data
            return jsonify(
                status="success",
                debugMessage=f"You allocated workers to {excess_worker_form.goal.choices[county.production_choice]}"
            )
        return jsonify(
            status="fail",
            debugMessage="Your allocation form failed to pass validation."
        )
