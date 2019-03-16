from copy import deepcopy

from undyingkingdoms.static.metadata.metadata_armies_all import generic_armies

elf_armies = deepcopy(generic_armies)
# First the strings and descriptions
elf_armies['peasant'].class_name, elf_armies['peasant'].class_name_plural, elf_armies[
    'peasant'].description = 'defender', 'defenders', 'They excel at repelling enemy armies.'
elf_armies['soldier'].class_name, elf_armies['soldier'].class_name_plural, elf_armies[
    'soldier'].description = 'ranger', 'rangers', 'Excellent offensive troops.'
elf_armies['archer'].class_name, elf_armies['archer'].class_name_plural, elf_armies[
    'archer'].description = 'longbowman', 'longbowmen', 'Longbowmen are very effective at defending your county.'
elf_armies['elite'].class_name, elf_armies['elite'].class_name_plural, elf_armies[
    'elite'].description = 'dragonhelm', 'dragonhelms', 'Dragonhelms are elite cavalry and incredibly adept at attacking enemy counties.'
elf_armies['monster'].class_name, elf_armies['monster'].class_name_plural, elf_armies[
    'monster'].description = 'dragon', 'dragons', 'Dragons are incredibly powerful monsters.'
# Elves: Slightly more damage and wood
# Peasants
elf_armies['peasant'].category = "Infantry"
elf_armies['peasant'].armour_type = "Unarmoured"
elf_armies['peasant'].health += 1
elf_armies['peasant'].wood += 2
# Soldiers
elf_armies['soldier'].category = "Infantry"
elf_armies['soldier'].armour_type = "Leather"
elf_armies['soldier'].health += 1
elf_armies['soldier'].wood += 2
# Archers
elf_armies['archer'].category = "Infantry"
elf_armies['archer'].armour_type = "Leather"
elf_armies['archer'].health += 1
elf_armies['archer'].wood += 3
# Elites
elf_armies['elite'].category = "Cavalry"
elf_armies['elite'].armour_type = "Plate"
elf_armies['elite'].attack += 1
elf_armies['elite'].defence += 1
elf_armies['elite'].wood += 4
# Monsters
elf_armies['monster'].category = "Monster"
elf_armies['monster'].armour_type = "Plate"
elf_armies['elite'].attack += 1
elf_armies['elite'].defence += 1
elf_armies['elite'].wood += 4
