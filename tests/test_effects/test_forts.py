from undyingkingdoms.models.counties.counties import County


def test_fort_multiplier(ctx):
    county = County.query.filter_by(leader="Haldon").one()
    infrastructure = county.infrastructure
    fort = county.buildings['fort']
    original_output = fort.output

    infrastructure.fort_multiplier = 0.5
    assert fort.output == round(original_output * 0.5)

    infrastructure.fort_multiplier = 2
    assert fort.output == round(original_output * 2)

    infrastructure.fort_multiplier = 1.6
    assert fort.output == round(original_output * 1.6)

