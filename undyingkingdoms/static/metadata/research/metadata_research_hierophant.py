from undyingkingdoms.models.technologies import Technology

hierophant_technology = {
    Technology(
        name='Sacrifice',
        cost=500,
        tier=1,
        max_level=1,
        description='Each thieves den grants an additional thief.'),
}

hierophant_technology = {
    tech.name: tech
    for tech in hierophant_technology
}
