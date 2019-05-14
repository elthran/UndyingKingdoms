from undyingkingdoms.models.exports import County


def test_economy_column_hoisting(ctx):
    county = County.query.get(1)
    economy = county.economy

    assert county.grain_produced == economy.grain_produced
    assert county.grain_modifier == economy.grain_modifier
    assert county.grain_produced != county.grain_modifier


def test_hoist_bug():
    class County:
        def __init__(self, economy):
            self.economy = economy

    class Economy:
        @property
        def grain_produced(self):
            return "grain_produced"

        @property
        def grain_modifier(self):
            return "grain_modifier"

    def hoist_names(cls_a, cls_b, names_to_hoist):
        for name in names_to_hoist:
            @property
            def func(self, name=name):
                return getattr(
                    getattr(self, cls_b.__name__.lower()),
                    name
                )

            setattr(cls_a, name, func)

    names_to_hoist = ['grain_produced', 'grain_modifier']
    hoist_names(County, Economy, names_to_hoist)

    economy = Economy()
    county = County(economy)

    assert county.grain_produced == economy.grain_produced
    assert county.grain_modifier == economy.grain_modifier
    assert county.grain_produced != county.grain_modifier


if __name__ == "__main__":
    test_hoist_bug()
