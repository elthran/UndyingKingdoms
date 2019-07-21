from importlib import import_module

from flask import jsonify
from flask.views import MethodView
from flask_login import login_required, current_user

get_forms = lambda: import_module('app.models.forms.infrastructure')
get_models = lambda: import_module('app.models.exports')
from app.metadata.metadata import all_buildings


class BuildBuildingsAPI(MethodView):
    @login_required
    def post(self):
        forms = get_forms()
        models = get_models()
        county = current_user.county
        infrastructure = county.infrastructure
        world = county.kingdom.world

        build_form = forms.InfrastructureForm()
        build_form.county_id.data = county.id

        if build_form.validate_on_submit():
            transaction = models.Transaction(county.id, county.day, world.day, "buy")
            for building in all_buildings:
                if build_form.data[building] > 0:
                    county.gold -= build_form.data[building] * infrastructure.buildings[building].gold_cost
                    county.wood -= build_form.data[building] * infrastructure.buildings[building].wood_cost
                    county.stone -= build_form.data[building] * infrastructure.buildings[building].stone_cost
                    infrastructure.buildings[building].pending += build_form.data[building]
                    transaction.add_purchase(
                        item_name=building,
                        item_amount=build_form.data[building],
                        gold_per_item=infrastructure.buildings[building].gold_cost,
                        wood_per_item=infrastructure.buildings[building].wood_cost,
                        stone_per_item=infrastructure.buildings[building].stone_cost
                    )
            transaction.save()
            return jsonify(
                status="success",
                debugMessage="You built some buildings."
            )
        return jsonify(
            status="fail",
            debugMessage="Your build buildings form did not pass validation."
        )
