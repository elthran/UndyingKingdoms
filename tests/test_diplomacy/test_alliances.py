from undyingkingdoms.models.exports import Diplomacy, Kingdom

def test_pending_alliances(ctx):
    faenoth = Kingdom.query.get(1)
    ecthalion = Kingdom.query.get(2)
    alliance = Diplomacy(faenoth, ecthalion, action=Diplomacy.ALLIANCE)
    alliance.save()

    assert len(faenoth._pending_alliances_you_started) == 1
    assert len(faenoth._pending_alliances_started_with_you) == 0
    assert len(faenoth.pending_alliances) == 1
    assert len(faenoth.kingdoms_who_we_offered_alliances_to) == 1
    assert len(faenoth.kingdoms_who_offered_us_alliances) == 0
