from flask import jsonify
from flask.views import MethodView
from flask_login import login_required, current_user


class CountyDescriptionAPI(MethodView):
    @login_required
    def get(self):
        county = current_user.county

        return jsonify(
            status="success",
            message=f"You called on {__name__}",
            race=county.race,
            name=county.name,
            title=county.title,
            leader=county.leader,
            background=county.background
        )
