from app.models.exports import Kingdom, Diplomacy


def test_armistice(ctx):
    faenoth = Kingdom.query.get(1)
    ecthalion = Kingdom.query.get(2)
    armistice = Diplomacy(faenoth, ecthalion, action=Diplomacy.ARMISTICE, status=Diplomacy.IN_PROGRESS)
    armistice.save()

    assert len(faenoth.kingdoms_in_armistice) == 1
    assert len(ecthalion.kingdoms_in_armistice) == 1
    assert faenoth.kingdoms_in_armistice != ecthalion.kingdoms_in_armistice
    assert faenoth.kingdoms_in_armistice == [ecthalion]
    assert ecthalion.kingdoms_in_armistice == [faenoth]

    assert len(faenoth.armistices) == 1
    assert len(ecthalion.armistices) == 1
    assert faenoth.armistices == ecthalion.armistices
