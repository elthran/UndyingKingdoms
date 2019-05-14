from undyingkingdoms.models.counties.counties import County


def test_fort_multiplier(ctx):
    county = County.query.filter_by(leader="Haldon").one()
    infrastructure = county.infrastructure

    fort_output = county.buildings['fort'].output
    infrastructure.fort_multiplier = 2

    assert county.buildings['fort'].output == fort_output * 2

    infrastructure.fort_multiplier = 1.6

    assert county.buildings['fort'].output == fort_output * 1.6

    infrastructure.fort_multiplier = 0.2

    assert county.buildings['fort'].output == fort_output * 0.2
