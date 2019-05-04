from undyingkingdoms.models.technologies import Technology

wizard_technology = [
    Technology(
        name='Spell Crafting',
        cost=500,
        max_level=1,
        description='Each thieves den grants an additional thief.'),
]

wizard_technology = {
    tech.key: tech
    for tech in wizard_technology
}
