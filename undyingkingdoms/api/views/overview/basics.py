from flask import jsonify
from flask.views import MethodView
from flask_login import login_required, current_user


class BasicsAPI(MethodView):
    @login_required
    def get(self):
        county = current_user.county
        preferences = county.preferences
        kingdom = county.kingdom
        world = kingdom.world

        return jsonify(
            status="success",
            debugMessage=f"You called on {__name__}",
            leaderless=kingdom.leader == 0,
            day=world.day,
            weather=preferences.weather.title(),
            land=county.land,
            season=world.season,
            end=210  # set round end.
        )
