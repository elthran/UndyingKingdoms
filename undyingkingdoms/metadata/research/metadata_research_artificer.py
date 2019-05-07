from undyingkingdoms.models.technologies import Technology

artificer_technology = {
    Technology(
        name='Mining',
        cost=750,
        max_level=2,
        description='You generate +{output:.0f} additional iron ore each day per level.',
        output=5
    ),
}

artificer_technology = {
    tech.key: tech
    for tech in artificer_technology
}
