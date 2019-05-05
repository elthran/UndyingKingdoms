from private_config import JACOB_TEMPORARY_EMAIL, JACOB_TEMPORARY_ACCOUNT_PASSWORD, MARLEN_TEMPORARY_EMAIL, \
    MARLEN_TEMPORARY_ACCOUNT_PASSWORD
from tests.fakes.providers import fake
from undyingkingdoms import User
from undyingkingdoms.controler.initialize import initialize_county
from undyingkingdoms.models.exports import World, Kingdom, County, Technology
from undyingkingdoms.models.forum import Forum, Thread
from undyingkingdoms.models.exports import Preferences
from undyingkingdoms.metadata.metadata import kingdom_names
from undyingkingdoms.metadata.research.metadata_research_all import generic_requirements


def build_testing_objects():
    world = World()
    world.save()
    # Create all the kingdoms
    for i in range(len(kingdom_names)):
        kingdom = Kingdom(kingdom_names[i])
        kingdom.save()
    # Create Elthran
    kingdom1 = Kingdom.query.get(1)
    user = User("elthran", JACOB_TEMPORARY_EMAIL, JACOB_TEMPORARY_ACCOUNT_PASSWORD)
    user.is_admin = True
    user.is_active = True
    user.is_verified = True
    county = initialize_county(user, kingdom1, "Ulthuan", "Elthran", 'Wizard','Ogre', 'Sir')
    county.save()
    county.vote = county.id
    county.buildings['arcane'].total = 5
    county.technologies['arcane knowledge'].completed = True
    county.buildings['lab'].total = 100
    # county.technologies['arcane knowledge II'].completed = True
    # county.technologies['arcane knowledge III'].completed = True
    county.mana = 500
    county.happiness = 80
    kingdom1.leader = county.id
    kingdom1.approval_rating = 60
    # Create Haldon
    kingdom2 = Kingdom.query.get(2)
    user = User("haldon", MARLEN_TEMPORARY_EMAIL, MARLEN_TEMPORARY_ACCOUNT_PASSWORD)
    user.is_admin = True
    user.is_active = True
    user.is_verified = True
    county = initialize_county(user, kingdom2, "Northern Wastes", "Haldon", 'Merchant', 'Human', 'Sir')
    county.save()
    county.vote = county.id
    county.buildings['arcane'].total = 5
    county.technologies['arcane knowledge'].completed = True
    # county.technologies['arcane knowledge II'].completed = True
    # county.technologies['arcane knowledge III'].completed = True
    county.mana = 500
    county.happiness = 80
    county.iron = 200
    county.buildings['lair'].total = 1
    county.armies['elite'].total = 100
    county.buildings['tavern'].total = 5
    county.population += 500
    kingdom2.leader = county.id
    kingdom2.approval_rating = 60
    # Create AI1 (He is weak and easier to attack for testing)
    user = User("ai1", "1@gmail.com", "star", is_bot=True)
    county = initialize_county(user, kingdom1, "Robotica1", "Mr. Roboto1", 'Druid', 'Dwarf', 'Lady')
    county.save()
    county.vote = county.id
    county.armies['peasant'].amount = 0
    county.armies['archer'].amount = 0
    # Create AI2 (He is weak and easier to attack for testing)
    user = User("ai2", "2@gmail.com", "star", is_bot=True)
    county = initialize_county(user, kingdom2, "Robotica2", "Mr. Roboto2", 'Merchant', 'Elf', 'Lady')
    county.save()
    county.vote = county.id
    county.armies['peasant'].amount = 0
    county.armies['archer'].amount = 0
    # Create AI3 (He is weak and easier to attack for testing)
    user = User("ai3", "3@gmail.com", "star", is_bot=True)
    county = initialize_county(user, kingdom2, "Robotica3", "Mr. Roboto3", 'Hierophant', 'Human', 'Lady')
    county.save()
    county.vote = county.id
    county.armies['peasant'].amount = 0
    county.armies['archer'].amount = 0
    # Create user with no county
    user = User("lonely", "lonely@gmail.com", "star")
    user.is_verified = True
    user.save()
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
