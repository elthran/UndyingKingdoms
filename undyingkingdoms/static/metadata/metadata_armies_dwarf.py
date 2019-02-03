from copy import deepcopy

from undyingkingdoms.static.metadata.metadata_armies_all import generic_armies

dwarf_armies = deepcopy(generic_armies)

# First the strings and descriptions
dwarf_armies['peasant'].class_name, dwarf_armies['peasant'].class_name_plural, dwarf_armies[
    'peasant'].description = 'miner', 'miners', 'Miners deal extra damage when attacking.'
dwarf_armies['soldier'].class_name, dwarf_armies['soldier'].class_name_plural, dwarf_armies[
    'soldier'].description = 'axeman', 'axemen', 'Excellent offensive troops.'
dwarf_armies['archer'].class_name, dwarf_armies['archer'].class_name_plural, dwarf_armies[
    'archer'].description = 'rifleman', 'riflemen', 'Dwarf riflemen are a powerful defensive force.'
dwarf_armies['elite'].class_name, dwarf_armies['elite'].class_name_plural, dwarf_armies[
    'elite'].description = 'greybeard', 'greybeards', 'Greybeards are capable of defending, as well as attacking.'

# Dwarves: Slightly higher health and iron
# Peasants
dwarf_armies['peasant'].gold += 3
dwarf_armies['peasant'].iron += 1
dwarf_armies['peasant'].attack += 1
dwarf_armies['peasant'].health += 1
# Soldiers
dwarf_armies['soldier'].iron += 1
dwarf_armies['soldier'].health += 1
# Archers
dwarf_armies['archer'].iron += 1
dwarf_armies['archer'].health += 1
# Elites
dwarf_armies['elite'].iron += 2
dwarf_armies['elite'].health += 2

