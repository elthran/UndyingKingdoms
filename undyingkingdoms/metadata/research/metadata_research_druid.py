from undyingkingdoms.models.technologies import Technology

druid_technology = {
    Technology(
        name='Nature',
        cost=500,
        max_level=1,
        description='Each thieves den grants an additional thief.'
    ),
}

druid_technology = {
    tech.key: tech
    for tech in druid_technology
}
