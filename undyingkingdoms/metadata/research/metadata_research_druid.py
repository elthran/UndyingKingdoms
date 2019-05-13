from undyingkingdoms.models.effects import Add
from undyingkingdoms.models.technologies import Technology

druid_technology = {
    Technology(
        name='Advanced Agriculture',
        cost=500,
        max_level=1,
        description="{grain_modifier:+0.0%} grain produced from each field",
        effects=Add(grain_modifier=0.50),
        source="Druid"
    ),
    Technology(
        name="Nature's Blessing",
        cost=1500,
        max_level=1,
        description='Your people are immune to sickness.',
        effects=None,
        source="Druid"
    )
}

# it must be a list or it will fail
custom_requirements = {
    "advanced agriculture": ["basic agriculture iii"],
    "nature's blessing": ["advanced agriculture"]
}

druid_technology = {
    tech.key: tech
    for tech in druid_technology
}
