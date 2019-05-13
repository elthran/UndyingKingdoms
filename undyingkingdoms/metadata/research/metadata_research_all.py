from undyingkingdoms.models.technologies.helpers import generate_tech_levels
from undyingkingdoms.models.technologies import Technology
from undyingkingdoms.models.effects import Add

generic_technology = [
    Technology(
        name='Basic Alchemy',
        cost=250,
        max_level=5,
        description='Generate an additional +{research_change} research each day.',
        effects=Add(research_change=10),
    ),
    Technology(
        name='Philosopher\'s Stone',
        cost=750,
        max_level=1,
        description='Generate an additional +4 gold for each mine you own.',
        effects=None,
    ),
    Technology(
        name='Basic Engineering',
        cost=250,
        max_level=5,
        description='+{build_slots} building can be built each day for each level.',
        effects=Add(build_slots=1)
    ),
    Technology(
        name='Public Works',
        cost=750,
        max_level=1,
        description='Your county generates an additional +{happiness_change} happiness each day.',
        effects=Add(happiness_change=1)
    ),
    Technology(
        name='Philosophy',
        cost=500,
        max_level=3,
        description='Your county generates an additional +{happiness_change} happiness each day.',
        effects=Add(happiness_change=1)
    ),
    Technology(
        name='Fertility',
        cost=1000,
        max_level=1,
        description='Your county has {birth_rate_modifier:+0.0%} to its birth rate',
        effects=Add(birth_rate_modifier=15)  # ?? +15%
    ),
    Technology(
        name='basic diplomacy',
        cost=5,
        max_level=1,
        description='???',
        effects=None
    ),
    Technology(
        name='advanced diplomacy',
        cost=5,
        max_level=1,
        description='???',
        effects=None
    ),
    Technology(
        name='Basic Agriculture',
        cost=250,
        max_level=3,
        description="{grain_modifier:+0.0%} grain produced from each field",
        effects=Add(grain_modifier=0.25)
    ),
    Technology(
        name='Animal Husbandry',
        cost=750,
        max_level=1,
        description='{dairy_modifier:+0.0%} bonus to all dairy production within your county.',
        effects=Add(dairy_modifier=0.50)
    ),
    Technology(
        name='basic hierophant',
        cost=5,
        max_level=1,
        description='???.',
        effects=None
    ),
    Technology(
        name='advanced hierophant',
        cost=5,
        max_level=1,
        description='???',
        effects=None
    ),
    Technology(
        name='Basic Economics',
        cost=250,
        max_level=5,
        description="Your county gets +10% bonus gold on all income",
        effects=None
    ),
    Technology(
        name='Banking',
        cost=750,
        max_level=1,
        description='Your banks generate an additional 6 gold each.',
        effects=Add(dairy_modifier=0.50)
    ),
    Technology(
        name='Basic Espionage',
        cost=250,
        max_level=5,
        description="An additional thief can be sent on each mission",
        effects=None
    ),
    Technology(
        name='Infiltration',
        cost=750,
        max_level=1,
        description='Each tavern can train an additional thief.',
        effects=None
    ),
    Technology(
        name='Basic Logistics',
        cost=250,
        max_level=3,
        description='Your armies return from battle {speed} day sooner.',
        effects=Add(speed=1)
    ),
    Technology(
        name='Military Training',
        cost=750,
        max_level=1,
        description='All your units have -1 upkeep',
        effects=None
    ),
    Technology(
        name='Basic Channelling',
        cost=250,
        max_level=5,
        description='Each level raises your maximum mana by {max_mana}.',
        effects=Add(max_mana=10)
    ),
    Technology(
        name='Attunement',
        cost=1000,
        max_level=1,
        description='Each level raises your mana generation per day by {mana_change}.',
        effects=Add(mana_change=1),
    )
]

custom_requirements = {
    "philosopher's stone": ["basic alchemy"],
    "public works": ["basic engineering"],
    "fertility": ["philosophy"],
    "advanced diplomacy": ["basic diplomacy"],
    "animal husbandry": ["basic agriculture"],
    "advanced hierophant": ["basic hierophant"],
    "banking": ["basic economics"],
    "infiltration": ["basic espionage"],
    "military training": ["basic logistics"],
    "attunement": ["basic channelling"]
}

generic_technology, generic_requirements = generate_tech_levels(generic_technology, custom_requirements)

# for tech in generic_technology.values():
#     print(tech.description)
"""
Technology(
    name='Masonry',
    cost=750,
    max_level=2,
    description="You generate +{iron_produced} additional iron ore each day per level.",
    output=5,
    effects=Add(iron_produced=5),
    source="Artificer"
)
"""
