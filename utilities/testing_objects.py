from private_config import JACOB_TEMPORARY_EMAIL, JACOB_TEMPORARY_ACCOUNT_PASSWORD, MARLEN_TEMPORARY_EMAIL, \
    MARLEN_TEMPORARY_ACCOUNT_PASSWORD
from undyingkingdoms import User
from undyingkingdoms.models import World, Kingdom, County
from undyingkingdoms.models.forum import Forum, Thread
from undyingkingdoms.models.preferences import Preferences
from undyingkingdoms.static.metadata.metadata import kingdom_names


def build_testing_objects():
    world = World()
    world.save()
    # Create all the kingdoms
    for i in range(len(kingdom_names)):
        kingdom = Kingdom(kingdom_names[i])
        kingdom.save()
    # Create Elthran
    user = User("elthran", JACOB_TEMPORARY_EMAIL, JACOB_TEMPORARY_ACCOUNT_PASSWORD)
    user.is_admin = True
    user.is_active = True
    user.save()
    county = County(1, "Ulthuan", "Elthran", user.id, 'Goblin', 'Sir', 'Merchant')
    county.save()
    county.vote = county.id
    county.kingdom_id = 1
    county.buildings['arcane'].total = 5
    county.technologies['arcane knowledge I'].completed = True
    county.technologies['arcane knowledge II'].completed = True
    county.technologies['arcane knowledge III'].completed = True
    county.mana = 500
    county.happiness = 80
    preferences = Preferences(county.id, user.id)
    preferences.save()
    kingdom = Kingdom.query.get(1)
    kingdom.leader = county.id
    # Create Haldon
    user = User("haldon", MARLEN_TEMPORARY_EMAIL, MARLEN_TEMPORARY_ACCOUNT_PASSWORD)
    user.is_admin = True
    user.is_active = True
    user.save()
    county = County(1, "Northern Wastes", "Haldon", user.id, 'Dwarf', 'Sir', 'Merchant')
    county.save()
    county.vote = county.id
    county.kingdom_id = 2
    county.buildings['arcane'].total = 5
    county.technologies['arcane knowledge I'].completed = True
    county.technologies['arcane knowledge II'].completed = True
    county.technologies['arcane knowledge III'].completed = True
    county.mana = 500
    county.happiness = 80
    county.iron = 200
    county.buildings['lair'].total = 1
    county.armies['elite'].total = 100
    county.buildings['tavern'].total = 5
    county.population += 500
    preferences = Preferences(county.id, user.id)
    preferences.save()
    kingdom = Kingdom.query.get(2)
    kingdom.leader = county.id
    # Create AI1 (He is weak and easier to attack for testing)
    user = User("ai1", "1@gmail.com", "star", is_bot=True)
    user.save()
    county = County(1, "Robotica1", "Mr. Roboto1", user.id, 'Dwarf', 'Lady', 'Engineer')
    county.save()
    county.vote = county.id
    county.armies['peasant'].amount = 0
    county.armies['archer'].amount = 0
    preferences = Preferences(county.id, user.id)
    preferences.save()
    # Create AI2 (He is weak and easier to attack for testing)
    user = User("ai2", "2@gmail.com", "star", is_bot=True)
    user.save()
    county = County(2, "Robotica2", "Mr. Roboto2", user.id, 'Elf', 'Lady', 'Engineer')
    county.save()
    county.vote = county.id
    county.armies['peasant'].amount = 0
    county.armies['archer'].amount = 0
    preferences = Preferences(county.id, user.id)
    preferences.save()
    # Create AI3 (He is weak and easier to attack for testing)
    user = User("ai3", "3@gmail.com", "star", is_bot=True)
    user.save()
    county = County(2, "Robotica3", "Mr. Roboto3", user.id, 'Human', 'Lady', 'Engineer')
    county.save()
    county.vote = county.id
    county.kingdom_id = 3
    county.armies['peasant'].amount = 0
    county.armies['archer'].amount = 0
    preferences = Preferences(county.id, user.id)
    preferences.save()
    # Create Forum shell
    forum = Forum()
    forum.save()
    thread = Thread(forum.id, "General", 1)
    thread.save()
    thread = Thread(forum.id, "Feedback & Suggestions", 1)
    thread.save()
    thread = Thread(forum.id, "Bug Reports", 1)
    thread.save()
    thread = Thread(forum.id, "Weekly Art Competition", 1)
    thread.save()
    thread = Thread(forum.id, "Monthly Feature Vote", 1)
    thread.save()
