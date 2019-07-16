from copy import deepcopy

from app.metadata.armies.metadata_armies_all import generic_armies

goblin_armies = deepcopy(generic_armies)
# First the strings and descriptions
goblin_armies['peasant'].class_name, goblin_armies['peasant'].class_name_plural, goblin_armies[
    'peasant'].description = 'slave', 'slaves', 'Slaves are cheap and expendable.'
goblin_armies['soldier'].class_name, goblin_armies['soldier'].class_name_plural, goblin_armies[
    'soldier'].description = 'berserker', 'berserkers', 'Soldiers are a solid offensive troop.'
goblin_armies['archer'].class_name, goblin_armies['archer'].class_name_plural, goblin_armies[
    'archer'].description = 'bowman', 'bowmen', 'Goblin archers are weaker than other archers but much cheaper.'
goblin_armies['besieger'].class_name, goblin_armies['besieger'].class_name_plural, goblin_armies[
    'besieger'].description = 'Catapult', 'Catapults', 'Catapults are incredibly effective at attacking fortified counties.'
goblin_armies['elite'].class_name, goblin_armies['elite'].class_name_plural, goblin_armies[
    'elite'].description = 'wolf rider', 'wolf riders', 'In large numbers, wolf riders are incredibly powerful.'
goblin_armies['monster'].class_name, goblin_armies['monster'].class_name_plural, goblin_armies[
    'monster'].description = 'wyvern', 'wyverns', 'Wyverns are devastating to any who cross their path.'
# Goblins: Lower health and damage, also lower costs
# Peasants
goblin_armies['peasant'].category = "Infantry"
goblin_armies['peasant'].armour_type = "Unarmoured"
# Soldiers
goblin_armies['soldier'].category = "Infantry"
goblin_armies['soldier'].armour_type = "Leather"
# Archers
goblin_armies['archer'].category = "Infantry"
goblin_armies['archer'].armour_type = "Leather"
goblin_armies['archer'].defence -= 1
goblin_armies['archer'].total += 5
goblin_armies['archer'].gold -= 5
goblin_armies['archer'].wood -= 1
goblin_armies['archer'].iron -= 1
goblin_armies['archer'].upkeep -= 5
# Besiegers
goblin_armies['besieger'].category = "Siege"
goblin_armies['besieger'].armour_type = "Plate"
# Elites
goblin_armies['elite'].category = "Cavalry"
goblin_armies['elite'].armour_type = "Plate"
# Monsters
goblin_armies['monster'].category = "Monster"
goblin_armies['monster'].armour_type = "Plate"
goblin_armies['monster'].ability = "Noxious Fumes"
goblin_armies['monster'].ability_description = f"When attacking, each {goblin_armies['monster'].class_name} " \
    f"causes a disease to plague the enemy county for an additional day."
