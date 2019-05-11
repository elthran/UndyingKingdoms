from undyingkingdoms.models.exports import Diplomacy, Kingdom


def test_war_victory_credit(app):
    with app.app_context():
        faenoth = Kingdom.query.get(1)
        ecthalion = Kingdom.query.get(2)

        war = faenoth.declare_war_against(ecthalion)
