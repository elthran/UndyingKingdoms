if __name__ == "__main__":
    """Allow running just this test.
    
    Usage: python tests/some_folder/somefile.py
    """

    import os
    os.system(f"python3 -m pytest -vv {__file__}")
    exit(1)  # prevents code from trying to run file afterwards.


from undyingkingdoms.models.forms.attack import AttackForm
from undyingkingdoms.models.users import User


def test_attack_form_validation(app):
    with app.app_context():
        user = User.query.first()
        form = AttackForm()

        peasant = user.county.armies['peasant'].available + 1
        soldier = user.county.armies['soldier'].available + 1
        besieger = user.county.armies['besieger'].available + 1
        summon = user.county.armies['summon'].available + 1
        elite = user.county.armies['elite'].available + 1
        monster = user.county.armies['monster'].available + 1

        form.peasant.choices = [(amount, amount) for amount in range(peasant)]
        form.soldier.choices = [(amount, amount) for amount in range(soldier)]
        form.besieger.choices = [(amount, amount) for amount in range(besieger)]
        form.summon.choices = [(amount, amount) for amount in range(summon)]
        form.elite.choices = [(amount, amount) for amount in range(elite)]
        form.monster.choices = [(amount, amount) for amount in range(monster)]

        form.peasant.data = 10
        form.soldier.data = 0
        form.besieger.data = 0
        form.summon.data = 0
        form.elite.data = 0
        form.monster.data = 0

        raise Warning("Attack form has more variables, this test is out of date.")
        if not form.validate():
            print(form.errors)
            assert 'Must send at least 25 troops.' in form.errors['peasant']
