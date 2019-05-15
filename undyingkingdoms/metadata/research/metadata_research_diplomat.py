from undyingkingdoms.models.effects import Times
from undyingkingdoms.models.technologies import Technology
from undyingkingdoms.models.technologies.helpers import generate_tech_levels

diplomat_technology = {
    Technology(
        name='diplo',
        cost=5,
        max_level=1,
        description='...',
        effects=None,
        source="Diplomat"
    ),
    Technology(
        name='diplo2',
        cost=5,
        max_level=1,
        description='...',
        effects=None,
        source="Diplomat"
    )
}

# it must be a list or it will fail
custom_requirements = {
}

diplomat_technology, diplomat_requirements = generate_tech_levels(diplomat_technology, custom_requirements)
