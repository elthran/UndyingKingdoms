from undyingkingdoms.models.technologies import Technology

ogre_technology = {
    Technology(
        name='Sharpened Sticks',
        cost=500,
        tier=1,
        max_level=1,
        description='Ogre brutes have an additional offense.'
    )
}

ogre_technology = {
    tech.key: tech
    for tech in ogre_technology
}
