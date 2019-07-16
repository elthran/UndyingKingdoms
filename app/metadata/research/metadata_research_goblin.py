from app.models.effects import Add
from app.models.technologies import Technology
from app.models.technologies.helpers import generate_tech_levels

goblin_technology = {
    Technology(
        name='Slavery',
        cost=1000,
        max_level=1,
        description='Your slaves are {abs(peasant_gold)} gold, {abs(peasant_wood)} wood, and {abs(peasant_iron)} iron cheaper. Also increases your excess production by a factor of {excess_production_multiplier}.',
        source="Goblin",
        effects=[Add('Military', peasant_gold=-5, peasant_wood=-1, peasant_iron=-1), Add('Economy', excess_production_multiplier=2)]
    ),
    Technology(
        name='Deathwish',
        cost=1000,
        max_level=1,
        description='Your berserkers have {soldier_attack:+} attack.',
        source="Goblin",
        effects=Add('Military', soldier_attack=1)
    ),
    Technology(
        name='Barbed Arrows',
        cost=1000,
        max_level=1,
        description='Your bowmen get {archer_defence:+} defence.',
        source="Goblin",
        effects=Add('Military', archer_defence=1)
    ),
    Technology(
        name='Cross-breeding',
        cost=1000,
        max_level=1,
        description='Wolf riders get {elite_attack:+} attack.',
        source="Goblin",
        effects=Add('Military', elite_attack=3)
    )
}

custom_requirements = {}

goblin_technology, goblin_requirements = generate_tech_levels(goblin_technology, custom_requirements)
