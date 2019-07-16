from app.models.exports import Kingdom


def test_war_victory_credit(ctx):
    faenoth = Kingdom.query.get(1)
    ecthalion = Kingdom.query.get(2)

    war = faenoth.declare_war_against(ecthalion)

    # test winning as aggressor (auto-win)
    assert faenoth.distribute_war_points(ecthalion, war.aggressor_goal) == True
    assert war.status == war.AGGRESSOR_WON

    # test winning as defender
    war = ecthalion.declare_war_against(faenoth)
    assert faenoth.distribute_war_points(ecthalion, war.defender_goal) == True
    assert war.status == war.DEFENDER_WON
