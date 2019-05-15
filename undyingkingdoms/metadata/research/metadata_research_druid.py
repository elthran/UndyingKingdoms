from undyingkingdoms.models.effects import Add
from undyingkingdoms.models.technologies import Technology
from undyingkingdoms.models.technologies.helpers import generate_tech_levels

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

druid_technology, druid_requirements = generate_tech_levels(druid_technology, custom_requirements)
