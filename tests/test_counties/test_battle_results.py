from undyingkingdoms.metadata.metadata import attack_types
from undyingkingdoms.models.exports import County
from undyingkingdoms.models.exports import User


def test_battle_results(app):
    with app.app_context():
        user1 = User('user1', 'user1@gmail.com', 'password')
        user1.save()
        county = County(1, "County1", "Leader1", user1, "Human", "Sir", "Merchant")
        county.save()

        army = dict(
            peasant=50,
            soldier=100,
            archer=0,
            besieger=0,
            summon=10,
            elite=10,
            monster=0
        )

        user2 = User('user2', 'user2@gmail.com', 'password')
        user2.save()
        county2 = County(1, "County2", "Leader2", user2, "Human", "Sir", "Merchant")
        county2.save()
        # create user 1
        # create user 2
        # simulate attack.
        result = county.battle_results(army, county2, attack_types[0])
        assert result  # is non null
