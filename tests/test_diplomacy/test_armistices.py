from undyingkingdoms.models.exports import Kingdom, Diplomacy


def test_armistice(ctx):
    faenoth = Kingdom.query.get(1)
    ecthalion = Kingdom.query.get(2)
    armistice = Diplomacy(faenoth, ecthalion, action=Diplomacy.ARMISTICE, status=Diplomacy.IN_PROGRESS)
    armistice.save()

    assert len(faenoth.armistices) == 1
    assert len(ecthalion.armistices) == 1
    assert faenoth.armistices != ecthalion.armistices
    assert faenoth.armistices == [ecthalion]
    assert ecthalion.armistices == [faenoth]
