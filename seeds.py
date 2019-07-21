from config import JACOB_TEMPORARY_EMAIL, JACOB_TEMPORARY_ACCOUNT_PASSWORD, MARLEN_TEMPORARY_EMAIL, \
    MARLEN_TEMPORARY_ACCOUNT_PASSWORD
from app.controler.initialize import initialize_county
from app.models.exports import World, Kingdom, User
from app.models.forum import Forum, Thread
from app.metadata.metadata import kingdom_names


def build_testing_objects():
    world = World()
    world.save()
    # Create all the kingdoms
    test_kingdom_names = kingdom_names + ["Empty"]
    for i in range(len(test_kingdom_names)):
        kingdom = Kingdom(test_kingdom_names[i])
        kingdom.save()
    # Create Elthran
    kingdom1 = Kingdom.query.get(1)
    user = User("elthran", JACOB_TEMPORARY_EMAIL, JACOB_TEMPORARY_ACCOUNT_PASSWORD)
    user.is_admin = True
    user.is_active = True
    user.is_verified = True
    county = initialize_county(user, kingdom1, "Ulthuan", 'Sir', "Elthran", 'Human', 'Rogue')
    county.save()
    county.vote = county.id
    infrastructure = county.infrastructure
    infrastructure.buildings['fort'].total = 10
    infrastructure.buildings['tavern'].total = 10
    county.armies['peasant'].total = 5000
    county.armies['monster'].total = 100
    county.armies['summon'].total = 100
    county.mana = 500
    county.happiness = 80
    kingdom1.leader = county.id
    county.technologies['basic espionage'].completed = True
    county.technologies['basic espionage ii'].completed = True
    county.technologies['basic espionage iii'].completed = True
    # county.technologies['elixir of life'].completed = True
    # Create Haldon
    kingdom2 = Kingdom.query.get(2)
    user = User("haldon", MARLEN_TEMPORARY_EMAIL, MARLEN_TEMPORARY_ACCOUNT_PASSWORD)
    user.is_admin = True
    user.is_active = True
    user.is_verified = True
    county = initialize_county(user, kingdom2, "Northern Wastes", 'Sir', "Haldon", 'Human', 'Druid')
    county.armies['summon'].total = 100
    county.save()
    county.vote = county.id
    infrastructure = county.infrastructure
    infrastructure.buildings['arcane'].total = 5
    infrastructure.buildings['lair'].total = 1
    infrastructure.buildings['tavern'].total = 5
    county.technologies['basic agriculture'].completed = True
    # county.technologies['basic agriculture II'].completed = True
    # county.technologies['basic agriculture III'].completed = True
    county.mana = 500
    county.happiness = 80
    county.iron = 200
    county.armies['elite'].total = 100
    county.population += 500
    # kingdom2.leader = county.id
    # kingdom2.approval_rating = 60
    # Create AI1 (He is weak and easier to attack for testing)
    user = User("ai1", "1@gmail.com", "star", is_bot=True)
    county = initialize_county(user, kingdom1, "Robotica1", 'Lady', "Mr. Roboto1", 'Dwarf', 'Druid')
    county.save()
    county.vote = county.id
    county.armies['peasant'].amount = 0
    county.armies['archer'].amount = 0
    # Create AI2 (He is weak and easier to attack for testing)
    user = User("ai2", "2@gmail.com", "star", is_bot=True)
    county = initialize_county(user, kingdom2, "Robotica2", 'Lady', "Mr. Roboto2", 'Elf', 'Merchant')
    county.save()
    county.vote = county.id
    county.armies['peasant'].amount = 0
    county.armies['archer'].amount = 0
    # Create AI3 (He is weak and easier to attack for testing)
    user = User("ai3", "3@gmail.com", "star", is_bot=True)
    county = initialize_county(user, kingdom2, "Robotica3", 'Lady', "Mr. Roboto3", 'Human', 'Hierophant')
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

    return locals()
