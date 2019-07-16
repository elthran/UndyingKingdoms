from tests import bp
from app.virtual_classes.all_metadata_imports import all_metadata_imports as md
from lib.namers import to_class_name

virtual_tech_classes = {}
for key in md:
    print(key.rsplit('_', maxsplit=1))
    discriminant = key.rsplit('_', maxsplit=1)[1]
    if 'research' in key:
        module = md[key]
        technologies = getattr(module, discriminant)
        for tech in technologies:
            cls_name = to_class_name(f'{tech.source} {tech.name}')
            print(
                f"""class {cls_name}:
    description = {tech.description}
"""
            )

bp()
