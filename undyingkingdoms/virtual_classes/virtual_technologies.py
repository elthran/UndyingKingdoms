from tests import bp
from undyingkingdoms.virtual_classes.all_metadata_imports import all_metadata_imports as md
from utilities.helpers import to_class_name

virtual_tech_classes = {}
for key in md:
    print(key.rsplit('_', maxsplit=1))
    discriminant = key.rsplit('_', maxsplit=1)[1]
    if 'research' in key:
        module = md[key]
        techs = getattr(module, discriminant)
        for tech in techs:
            cls_name = to_class_name(f'{tech.source} {tech.name}')
            print(
                f"""class {cls_name}:
    description = {tech.description}
"""
            )

bp()
