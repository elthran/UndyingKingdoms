from flask import jsonify
from flask.views import MethodView
from flask_login import login_required, current_user

from undyingkingdoms.api.vue_safe import vue_safe_form, generic_vue_safe


class UpdateAPI(MethodView):
    @login_required
    def get(self):
        county = current_user.county

        return jsonify(
            debugMessage=f"You called on {__name__}",
        )

    @login_required
    def post(self):
        county = current_user.county
        form = None

        if form.validate_on_submit():
            return jsonify(
                debugMessage='You have updated your current troop production.',
            ), 201
        return jsonify(
            debugMessage='Your troop production form did not pass validation.'
        ), 403
