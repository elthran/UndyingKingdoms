from flask import jsonify
from flask.views import MethodView
from flask_login import login_required, current_user

from app.models.exports import Transaction
from app.models.forms.infrastructure import InfrastructureForm
from app.metadata.metadata import all_buildings


class BuildBuildingsAPI(MethodView):
    @login_required
    def post(self):
        county = current_user.county
        world = county.kingdom.world

        build_form = InfrastructureForm()
        build_form.county_id.data = county.id

        if build_form.validate_on_submit():
            transaction = Transaction(county.id, county.day, world.day, "buy")
            for building in all_buildings:
                if build_form.data[building] > 0:
                    county.gold -= build_form.data[building] * county.buildings[building].gold_cost
                    county.wood -= build_form.data[building] * county.buildings[building].wood_cost
                    county.stone -= build_form.data[building] * county.buildings[building].stone_cost
                    county.buildings[building].pending += build_form.data[building]
                    transaction.add_purchase(
                        item_name=building,
                        item_amount=build_form.data[building],
                        gold_per_item=county.buildings[building].gold_cost,
                        wood_per_item=county.buildings[building].wood_cost,
                        stone_per_item=county.buildings[building].stone_cost
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
