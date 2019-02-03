from copy import deepcopy

from undyingkingdoms.static.metadata_all_races import generic_buildings, generic_armies

goblin_armies = deepcopy(generic_armies)
# First the strings and descriptions
goblin_armies['peasant'].class_name, goblin_armies['peasant'].class_name_plural = 'scout', 'scouts'
goblin_armies['peasant'].description = 'Scouts are cheap and expendable.'
goblin_armies['soldier'].class_name, goblin_armies['soldier'].class_name_plural = 'berserker', 'berserkers'
goblin_armies['soldier'].description = 'Soldiers are a solid offensive troop.'
goblin_armies['archer'].class_name, goblin_armies['archer'].class_name_plural = 'bowman', 'bowmen'
goblin_armies['archer'].description = 'Goblin archers are weaker than other archers but much cheaper.'
goblin_armies['elite'].class_name, goblin_armies['elite'].class_name_plural = 'wolf rider', 'wolf riders'
goblin_armies['elite'].description = 'In large numbers, wolf riders are incredibly powerful.'
# Goblins: Lower health and damage, also lower costs
# Peasants=
goblin_armies['peasant'].gold -= 1
goblin_armies['peasant'].iron -= 1
goblin_armies['peasant'].upkeep -= 1
# Soldiers
goblin_armies['soldier'].attack -= 1
goblin_armies['soldier'].health -= 1
goblin_armies['soldier'].gold -= 5
goblin_armies['soldier'].iron -= 2
goblin_armies['soldier'].upkeep -= 5
# Archers
goblin_armies['archer'].total += 5
goblin_armies['archer'].defence -= 1
goblin_armies['archer'].gold -= 5
goblin_armies['archer'].iron -= 2
goblin_armies['archer'].upkeep -= 5
# Elites
goblin_armies['elite'].attack -= 2
goblin_armies['elite'].defence -= 2
goblin_armies['elite'].health -= 1
goblin_armies['elite'].gold -= 10
goblin_armies['elite'].iron -= 5
goblin_armies['elite'].upkeep -= 5

goblin_buildings = generic_buildings
goblin_buildings['houses'].class_name = 'log cabin'

