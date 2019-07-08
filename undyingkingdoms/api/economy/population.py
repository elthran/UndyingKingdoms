from flask import jsonify
from flask.views import MethodView
from flask_login import login_required, current_user

from undyingkingdoms.serializers.vue_safe import vue_safe_metadata_mod
from undyingkingdoms.metadata.metadata import birth_rate_modifier


class PopulationAPI(MethodView):
    @login_required
    def get(self):
        county = current_user.county

        return jsonify(
            status='success',
            debugMessage='You called on the population api.',
            population=county.population,
            population_projection=county.get_population_change(),
            race=county.race,
            background=county.background,
            birth_rate=county.birth_rate,
            immigration_rate=county.immigration_rate,
            death_rate=county.get_death_rate(),
            emigration_rate=county.get_emigration_rate(),
            birth_rate_mod=vue_safe_metadata_mod(birth_rate_modifier, county),
        )
