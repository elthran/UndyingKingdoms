from undyingkingdoms.models.counties.specifics import merge_tech_requirements


def test_merge_tech_requirements():
    requirements = merge_tech_requirements('Ogre', 'Alchemist')

    assert 'elixir of life' in requirements
