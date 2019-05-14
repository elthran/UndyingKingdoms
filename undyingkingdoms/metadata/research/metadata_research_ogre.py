from undyingkingdoms.models.effects import Add
from undyingkingdoms.models.technologies import Technology

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

ogre_technology = {
    tech.key: tech
    for tech in ogre_technology
}
