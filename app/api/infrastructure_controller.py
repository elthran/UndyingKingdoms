from flask_login import current_user, login_required

from lib.base_controller import CRUDMethodView


class InfrastructureController(CRUDMethodView):
    @login_required
    def read(self):
        county = current_user.county
        infrastructure = county.infrastructure

        return dict(
            land_available=infrastructure.get_available_land(),
            land=county.land,
            citizens_available=county.get_available_workers(),
            citizens=county.population,
            citizens_needed=infrastructure.get_workers_needed_to_be_efficient(),
            efficiency=infrastructure.building_efficiencies(),
        ), 200

    def update(self):
        pass
