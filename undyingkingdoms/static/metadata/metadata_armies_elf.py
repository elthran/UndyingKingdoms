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
