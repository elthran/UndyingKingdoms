from tests import bp
from undyingkingdoms.models.exports import County


def test_technology_effects(app):
    with app.app_context():
        county = County.query.filter_by(leader="Haldon").one()
        output = county.grain_produced
        assert output == 400

        county.technologies['agriculture'].completed = True

        # bp()
        assert county.grain_produced == output * 1.25
