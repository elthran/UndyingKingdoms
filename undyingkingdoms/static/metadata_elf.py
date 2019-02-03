from copy import deepcopy

from undyingkingdoms.static.metadata_all_races import generic_buildings, generic_armies

elf_armies = deepcopy(generic_armies)
# First the strings and descriptions
elf_armies['peasant'].class_name, elf_armies['peasant'].class_name_plural = 'defender', 'defenders'
elf_armies['peasant'].description = 'They excel at repelling enemy armies.'
elf_armies['soldier'].class_name, elf_armies['soldier'].class_name_plural = 'ranger', 'rangers'
elf_armies['soldier'].description = 'Excellent offensive troops. '
elf_armies['archer'].class_name, elf_armies['archer'].class_name_plural = 'longbowman', 'longbowmen'
elf_armies['archer'].description = 'Longbowmen are very effective at defending your county.'
elf_armies['elite'].class_name, elf_armies['elite'].class_name_plural = 'dragonhelm', 'dragonhelms'
elf_armies['elite'].description = 'Dragonhelms are elite cavalry and incredibly adept at attacking enemy counties.'
# Elves: Slightly more damage and wood
# Peasants
elf_armies['peasant'].attack += 1
elf_armies['peasant'].defence += 1
elf_armies['peasant'].wood += 1
# Soldiers
elf_armies['soldier'].attack += 1
elf_armies['soldier'].wood += 2
# Archers
elf_armies['archer'].defence += 1
elf_armies['archer'].wood += 2
# Elites
elf_armies['elite'].attack += 1
elf_armies['elite'].defence += 1
elf_armies['elite'].wood += 3

elf_buildings = generic_buildings
elf_buildings['houses'].class_name = 'sanctuary'

