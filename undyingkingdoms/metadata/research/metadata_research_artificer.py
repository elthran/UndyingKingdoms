from undyingkingdoms.models.technologies import Technology

artificer_technology = {
    Technology(
        name='Engineering',
        cost=500,
        max_level=1,
        description='Each thieves den grants an additional thief.'
    ),
}

artificer_technology = {
    tech.key: tech
    for tech in artificer_technology
}
