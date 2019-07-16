from sqlalchemy.sql.functions import count

from app.models.exports import Kingdom
from app.models.forms.royal_court import RoyalCourtRelationsForm


def build_relations_form(kingdom):
    form = RoyalCourtRelationsForm()
    all_kingdoms = Kingdom.query.filter(Kingdom.id != kingdom.id).all()
    all_kingdoms = [kingdom for kingdom in all_kingdoms if len(kingdom.counties) > 0]

    kingdoms_at_war = kingdom.enemies
    kingdoms_at_peace = kingdom.allies + \
                        kingdom.kingdoms_with_pending_alliances + \
                        kingdom.kingdoms_in_armistice

    eligible_kingdoms = set(all_kingdoms) - set(kingdoms_at_war) - set(kingdoms_at_peace)

    form.target_id.choices = [(kingdom.id, kingdom.name) for kingdom in eligible_kingdoms]

    return form
