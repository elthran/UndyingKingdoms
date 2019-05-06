from undyingkingdoms.models.technologies import Technology

hierophant_technology = {
    Technology(
        name='Sacrifice',
        cost=500,
        max_level=1,
        description='All units gain +2 attack and -1 health.'),
}

hierophant_technology = {
    tech.key: tech
    for tech in hierophant_technology
}
