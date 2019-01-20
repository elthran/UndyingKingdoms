if __name__ == "__main__":
    """Allow running just this test.
    
    Usage: python tests/some_folder/somefile.py
    """

    import os
    os.system("python3 -m pytest -vv {}".format(__file__))
    exit(1)  # prevents code from trying to run file afterwards.


from undyingkingdoms.models.forms.attack import AttackForm
from undyingkingdoms.models.users import User


def test_attack_form_validation(app):
    with app.app_context():
        user = User.query.first()
        form = AttackForm()

        peasants = user.county.armies['peasant'].available + 1
        archers = user.county.armies['archer'].available + 1
        soldiers = user.county.armies['soldier'].available + 1
        elites = user.county.armies['elite'].available + 1

        form.peasant.choices = [(amount, amount) for amount in range(peasants)]
        form.archer.choices = [(amount, amount) for amount in range(archers)]
        form.soldier.choices = [(amount, amount) for amount in range(soldiers)]
        form.elite.choices = [(amount, amount) for amount in range(elites)]

        form.peasant.data = 10
        form.archer.data = 0
        form.soldier.data = 0
        form.elite.data = 0

        if not form.validate():
            print(form.errors)
            assert 'Must send at least 25 troops.' in form.errors['peasant']
