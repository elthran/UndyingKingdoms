from undyingkingdoms.models.technologies import Technology

merchant_technology = {
    Technology(
        name='Economics',
        cost=500,
        max_level=1,
        description='Each thieves den grants an additional thief.'
    ),
}

merchant_technology = {
    tech.key: tech
    for tech in merchant_technology
}
