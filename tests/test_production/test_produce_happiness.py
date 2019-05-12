from random import choice

from undyingkingdoms.models.exports import County


def test_produce_happiness(app):
    with app.app_context():
        county = County.query.get(1)

        assert county.production_choice != county.HAPPINESS

        current_change = county.happiness_change
        expected_change = county.get_excess_production_value(county.HAPPINESS)
        assert expected_change > 0

        county.production_choice = county.HAPPINESS

        assert current_change + expected_change == county.happiness_change

        current_change = county.happiness_change
        county.production_choice = choice([county.GOLD, county.LAND, county.FOOD])

        assert current_change - expected_change == county.happiness_change
