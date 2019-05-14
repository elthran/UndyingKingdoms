from undyingkingdoms.models.counties.counties import County


def test_infrastructure_cost_modifier(app):
    with app.app_context():
        county = County.query.filter_by(leader="Haldon").one()
        infrastructure = county.infrastructure

        gold_cost = county.buildings['lair'].gold_cost
        infrastructure.cost_modifier = 0.2

        assert county.buildings['lair'].gold_cost == round(gold_cost * 0.8)


