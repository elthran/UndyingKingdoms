from copy import deepcopy

from undyingkingdoms.static.metadata.metadata_armies_all import generic_armies

goblin_armies = deepcopy(generic_armies)
# First the strings and descriptions
goblin_armies['peasant'].class_name, goblin_armies['peasant'].class_name_plural, goblin_armies[
    'peasant'].description = 'scout', 'scouts', 'Scouts are cheap and expendable.'
goblin_armies['soldier'].class_name, goblin_armies['soldier'].class_name_plural, goblin_armies[
    'soldier'].description = 'berserker', 'berserkers', 'Soldiers are a solid offensive troop.'
goblin_armies['archer'].class_name, goblin_armies['archer'].class_name_plural, goblin_armies[
    'archer'].description = 'bowman', 'bowmen', 'Goblin archers are weaker than other archers but much cheaper.'
goblin_armies['elite'].class_name, goblin_armies['elite'].class_name_plural, goblin_armies[
    'elite'].description = 'wolf rider', 'wolf riders', 'In large numbers, wolf riders are incredibly powerful.'
goblin_armies['monster'].class_name, goblin_armies['monster'].class_name_plural, goblin_armies[
    'monster'].description = 'wyvern', 'wyverns', 'Wyverns are devastating to any who cross their path.'
# Goblins: Lower health and damage, also lower costs
# Peasants
goblin_armies['peasant'].category = "Infantry"
goblin_armies['peasant'].armour_type = "Unarmoured"
goblin_armies['peasant'].gold -= 2
goblin_armies['peasant'].iron -= 1
goblin_armies['peasant'].upkeep -= 1
goblin_armies['peasant'].defence -= 1
# Soldiers
goblin_armies['soldier'].category = "Infantry"
goblin_armies['soldier'].armour_type = "Leather"
goblin_armies['soldier'].defence -= 1
goblin_armies['soldier'].health -= 1
goblin_armies['soldier'].gold -= 5
goblin_armies['soldier'].iron -= 2
goblin_armies['soldier'].upkeep -= 5
# Archers
goblin_armies['archer'].category = "Infantry"
goblin_armies['archer'].armour_type = "Leather"
goblin_armies['archer'].total += 5
goblin_armies['archer'].defence -= 1
goblin_armies['archer'].gold -= 5
goblin_armies['archer'].iron -= 2
goblin_armies['archer'].upkeep -= 5
# Elites
goblin_armies['elite'].category = "Cavalry"
goblin_armies['elite'].armour_type = "Plate"
goblin_armies['elite'].attack -= 2
goblin_armies['elite'].defence -= 2
goblin_armies['elite'].health -= 1
goblin_armies['elite'].gold -= 10
goblin_armies['elite'].iron -= 4
goblin_armies['elite'].upkeep -= 5
# Monsters
goblin_armies['monster'].category = "Monster"
goblin_armies['monster'].armour_type = "Plate"
