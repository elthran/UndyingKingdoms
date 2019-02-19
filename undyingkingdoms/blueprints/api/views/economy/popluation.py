from flask import jsonify
from flask.views import MethodView
from flask_login import login_required, current_user

from undyingkingdoms.static.metadata.metadata import birth_rate_modifier


class PopulationAPI(MethodView):
    @login_required
    def get(self):
        county = current_user.county

        race_mod = birth_rate_modifier.get(county.race)
        background_mod = birth_rate_modifier.get(county.background)
        birth_rate_mod = {}
        if race_mod:
            birth_rate_mod['race'] = dict(
                name=race_mod[0],
                value=int(race_mod[1] * 100)
            )
        if background_mod:
            birth_rate_mod['background'] = dict(
                name=background_mod[0],
                value=int(background_mod[1] * 100)
            )

        data = dict(
            population=county.population,
            population_projection=county.get_population_change(prediction=True),
            birth_rate_mod=birth_rate_mod,
            race=county.race,
            background=county.background,
            birth_rate=county.get_birth_rate(),
            immigration_rate=county.get_immigration_rate(),
            death_rate=county.get_death_rate(),
            emigration_rate=county.get_emigration_rate()
        )

        return jsonify(
            status='success',
            message='You called on the population api.',
            county=data
        )
