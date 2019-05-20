from undyingkingdoms.models.counties.counties import County


def test_fort_multiplier(ctx):
    county = County.query.filter_by(leader="Haldon").one()
    infrastructure = county.infrastructure

    original_output = county.buildings['fort'].output


    infrastructure.fort_multiplier = 0.5
    halved_output = county.buildings['fort'].output

    infrastructure.fort_multiplier = 2
    doubled_output = county.buildings['fort'].output

    infrastructure.fort_multiplier = 1.6
    one_point_six_output = county.buildings['fort'].output

    assert doubled_output == original_output * 2

    assert halved_output == original_output * 0.5

    assert one_point_six_output == original_output * 1.6

