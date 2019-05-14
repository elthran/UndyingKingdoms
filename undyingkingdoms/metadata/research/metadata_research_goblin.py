from undyingkingdoms.models.effects import Add
from undyingkingdoms.models.technologies import Technology

goblin_technology = {
    Technology(
        name='Slavery',
        cost=1000,
        max_level=1,
        description='Your slaves are {abs(peasant_gold)} gold, {abs(peasant_wood)} wood, and {abs(peasant_iron)} iron cheaper.',
        source="Goblin",
        effects=Add('military', peasant_gold=-5, peasant_wood=-1, peasant_iron=-1)
    ),
    Technology(
        name='Deathwish',
        cost=1000,
        max_level=1,
        description='Your berserkers have +1 attack.',
        source="Goblin"
    ),
    Technology(
        name='Barbed Arrows',
        cost=1000,
        max_level=1,
        description='Your bowmen get +1 defence.',
        source="Goblin"
    ),
    Technology(
        name='Cross-breeding',
        cost=1000,
        max_level=1,
        description='Wolf riders get +3 attack.',
        source="Goblin"
    )
}


goblin_technology = {
    tech.key: tech
    for tech in goblin_technology
}
