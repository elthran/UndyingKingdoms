from undyingkingdoms.models.technologies import Technology

merchant_technology = {
    Technology(
        name='Mercantilism',
        cost=750,
        max_level=3,
        description='Increases all gold income by 10%.',
        output=0.1
    )
}

merchant_technology = {
    tech.key: tech
    for tech in merchant_technology
}
