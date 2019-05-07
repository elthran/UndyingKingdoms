from undyingkingdoms.models.exports import County


def test_economy_column_hoisting(app):
    with app.app_context():
        county = County.query.get(1)
        economy = county.economy

        assert county.grain_produced == economy.grain_produced
        assert county.grain_modifier == economy.grain_modifier
        assert county.grain_produced == county.grain_modifier
