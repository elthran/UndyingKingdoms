from undyingkingdoms.models.counties.counties import County


def test_technology_effects(app):
    with app.app_context():
        county = County.query.filter_by(leader="Haldon").one()
        output = county.grain_produced

        county.technologies['basic agriculture'].completed = True

        assert output < county.grain_produced

        county.technologies['basic agriculture'].completed = False

        assert county.grain_produced == output
