from undyingkingdoms.models.technologies import Technology

hierophant_technology = {
    Technology(
        name='Sacrifice',
        cost=5,
        max_level=1,
        description='...',
        effects=None,
        source="Hierophant"
    ),
    Technology(
        name='Sacrifice 2',
        cost=5,
        max_level=1,
        description='...',
        effects=None,
        source="Hierophant"
    )
}


# it must be a list or it will fail
custom_requirements = {
}

hierophant_technology = {
    tech.key: tech
    for tech in hierophant_technology
}
