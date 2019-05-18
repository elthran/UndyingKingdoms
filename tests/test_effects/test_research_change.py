from undyingkingdoms.models.counties.counties import County


def test_research_change(ctx):
    county = County.query.get(1)

    research_change = county.research_change

    county.technologies['basic alchemy'].completed = True

    assert county.research_change > research_change
