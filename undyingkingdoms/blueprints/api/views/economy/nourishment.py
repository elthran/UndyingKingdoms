from flask import jsonify
from flask.views import MethodView
from flask_login import login_required, current_user

from undyingkingdoms.blueprints.api.vue_safe import vue_safe_metadata_mod
from undyingkingdoms.static.metadata.metadata import happiness_modifier


class NourishmentAPI(MethodView):
    @login_required
    def get(self):
        county = current_user.county

        return jsonify(
            status='success',
            message='You called the nourishment api.',
            nourishment=county.nourishment,
            nourishmentChange=county.get_nourishment_change(),
        )
