from undyingkingdoms.models.effects import Plequals
from undyingkingdoms.models.technologies import Technology

artificer_technology = {
    Technology(
        name='Mining',
        cost=750,
        max_level=2,
        description='You generate +{iron_produced} additional iron ore each day per level.',
        output=5,
        effects=Plequals(iron_produced=5)
    ),
}

artificer_technology = {
    tech.key: tech
    for tech in artificer_technology
}
