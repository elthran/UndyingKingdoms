from flask import jsonify, url_for
from flask.views import MethodView
from flask_login import login_required, current_user

from .helpers import max_buildable_by_cost
from undyingkingdoms.models.forms.infrastructure import InfrastructureForm


class BuildingsAPI(MethodView):
    @login_required
    def get(self):
        county = current_user.county

        build_form = InfrastructureForm()

        form_data = dict(
            _action=url_for('api.infrastructure_build_buildings_api'),
            csrf_token=build_form.csrf_token.current_token,
            county_id=county.id
        )

        vue_safe_buildings = {}
        build_order = []
        total_built = 0
        total_pending = 0
        total_employed = 0
        for index, building in enumerate(county.buildings.values()):
            name = building.name
            build_order.append(name)
            form_data[name] = 0  # add all fields to form_data
            # import pdb;pdb.set_trace()
            max_size = max_buildable_by_cost(county, building)
            vue_safe_buildings[name] = dict(
                name=building.class_name.title(),
                total=building.total,
                pending=building.pending,
                amount=0,
                description=building.description,
                goldCost=building.gold_cost,
                woodCost=building.wood_cost,
                stoneCost=building.stone_cost,
                maxBuildable=max_size,
                buildChoices=[[n, n] for n in range(max_size+1)],
                totalEmployed=building.workers_employed * building.total,
                workersEmployed=building.workers_employed
            )
            total_built += vue_safe_buildings[name]['total']
            total_pending += vue_safe_buildings[name]['pending']
            total_employed += vue_safe_buildings[name]['totalEmployed']




        return jsonify(
            status="success",
            debugMessage="You called on the buildings api.",
            buildings=vue_safe_buildings,
            buildOrder=build_order,
            totalBuilt=total_built,
            totalPending=total_pending,
            totalEmployed=total_employed,
            formData=form_data
        )
