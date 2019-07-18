from app.models.counties.counties import County


def test_elixir_of_life(ctx):
    county = County.query.get(1)

    first_technology_name = next(iter(county.technologies))
    first_technology = county.technologies[first_technology_name]
    technology_is_available = first_technology in set(county.available_technologies)
    assert technology_is_available != (first_technology in county.unavailable_technologies)
