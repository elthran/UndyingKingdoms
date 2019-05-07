from undyingkingdoms.models.technologies import Technology

diplomat_technology = {
    Technology(
        name='Bartering',
        cost=500,
        max_level=1,
        description='Increases all gold income by 15%.',
        output=0.15
    ),
}

diplomat_technology = {
    tech.key: tech
    for tech in diplomat_technology
}
