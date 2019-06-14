from undyingkingdoms.models.exports import County


def test_advance_research(ctx):
    county = County.query.get(1)

    available_technologies = list(county.available_techs)

    # test research completes
    county.research = county.research_choice.cost
    county.advance_research()
    assert list(county.available_techs) != available_technologies

    # complete all technologies
    for tech in county.incomplete_techs:
        tech.completed = True
        tech.save()

    assert list(county.available_techs) == []
    county.research = county.research_choice.cost
    county.advance_research()

    assert county.research_choice is None
    assert county.research == 0

    # check gold increases when there are no more technologies.
    initial_gold = county.gold
    new_research = 100
    county.research = new_research
    county.advance_research()
    assert county.gold == initial_gold + new_research
