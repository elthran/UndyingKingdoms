from undyingkingdoms.models.counties.counties import County


def test_elixir_of_life(ctx):
    county = County.query.get(1)

    assert "elixir of life" in county.technologies
    elixir_of_life = county.technologies["elixir of life"]
    assert elixir_of_life not in county.available_technologies
    assert elixir_of_life in county.unavailable_technologies
