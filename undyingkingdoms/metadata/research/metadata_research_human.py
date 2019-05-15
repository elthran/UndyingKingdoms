from undyingkingdoms.models.effects import Times, Add
from undyingkingdoms.models.technologies import Technology
from undyingkingdoms.models.technologies.helpers import generate_tech_levels

human_technology = {
    Technology(
        name='Civic Duty',
        cost=500,
        max_level=1,
        description='Reduces upkeep cost of men-at-arms by {abs(peasant_upkeep)} gold each.',
        source="Human",
        effects=Add('military', peasant_upkeep=-10)
    ),
    Technology(
        name='Economics',
        cost=750,
        max_level=1,
        description='Increases all gold income by {gold_modifier:+0.0%}.',
        effects=Add('economy', gold_modifier=0.15),
        source="Human"
    ),
    Technology(
        name='Knights Templar',
        cost=1000,
        max_level=1,
        description='All knights get {elite_attack:+} attack.',
        source="Human",
        effects=Add('military', elite_attack=3)
    ),
    Technology(
        name='Trading',
        cost=750,
        max_level=1,
        description='All military units cost {abs(unit_gold)} less gold to train.',
        source="Human",
        effects=Add('military', unit_gold=-5)
    )
}

custom_requirements = {
}

human_technology, human_requirements = generate_tech_levels(human_technology, custom_requirements)
