from undyingkingdoms.models.technologies import Technology

hierophant_technology = {
    Technology(
        name='Sacrifice',
        cost=500,
        max_level=1,
        description='Each thieves den grants an additional thief.'),
}

hierophant_technology = {
    tech.key: tech
    for tech in hierophant_technology
}
