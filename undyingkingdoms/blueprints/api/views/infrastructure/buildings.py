from flask import jsonify, url_for
from flask.views import MethodView
from flask_login import login_required, current_user

from undyingkingdoms.blueprints.api.views.infrastructure.helpers import max_buildable_by_cost


class BuildingsAPI(MethodView):
    @login_required
    def get(self):
        county = current_user.county

        vue_safe_buildings = {}
        buildingsChoices = []
        total_built = 0
        total_pending = 0
        total_employed = 0
        for index, building in enumerate(county.buildings.values()):
            name = building.class_name.title()
            buildingsChoices.append([index, name])
            # import pdb;pdb.set_trace()
            vue_safe_buildings[name] = dict(
                total=building.total,
                pending=building.pending,
                description=building.description,
                goldCost=building.gold_cost,
                woodCost=building.wood_cost,
                stoneCost=building.stone_cost,
                maxBuildable=max_buildable_by_cost(county, building),
                totalEmployed=building.workers_employed * building.total,
                workersEmployed=building.workers_employed
            )
            total_built += vue_safe_buildings[name]['total']
            total_pending += vue_safe_buildings[name]['pending']
            total_employed += vue_safe_buildings[name]['totalEmployed']



        return jsonify(
            status="success",
            message="You called on the buildings api.",
            buildingsChoices=buildingsChoices,
            buildings=vue_safe_buildings,
            totalBuilt=total_built,
            totalPending=total_pending,
            totalEmployed=total_employed
        )
