from undyingkingdoms.models.effects import Add
from undyingkingdoms.models.technologies import Technology
from undyingkingdoms.models.technologies.helpers import generate_tech_levels

ogre_technology = {
    Technology(
        name='Sharpened Sticks',
        cost=500,
        max_level=1,
        description='Ogre brutes have an additional offense.',
        source="Ogre",
        effects=Add('military', peasant_attack=1)
    )
}

custom_requirements = {
}

ogre_technology, ogre_requirements = generate_tech_levels(ogre_technology, custom_requirements)
