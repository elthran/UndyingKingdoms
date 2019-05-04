from copy import deepcopy

from undyingkingdoms.metadata.armies.metadata_armies_all import generic_armies

dwarf_armies = deepcopy(generic_armies)

# First the strings and descriptions
dwarf_armies['peasant'].class_name, dwarf_armies['peasant'].class_name_plural, dwarf_armies[
    'peasant'].description = 'miner', 'miners', 'Miners deal extra damage when attacking.'
dwarf_armies['soldier'].class_name, dwarf_armies['soldier'].class_name_plural, dwarf_armies[
    'soldier'].description = 'axeman', 'axemen', 'Excellent offensive troops.'
dwarf_armies['archer'].class_name, dwarf_armies['archer'].class_name_plural, dwarf_armies[
    'archer'].description = 'rifleman', 'riflemen', 'Dwarf riflemen are a powerful defensive force.'
dwarf_armies['besieger'].class_name, dwarf_armies['besieger'].class_name_plural, dwarf_armies[
    'besieger'].description = 'cannon', 'cannons', 'Trebuchets are incredibly effective against fortified counties.'
dwarf_armies['elite'].class_name, dwarf_armies['elite'].class_name_plural, dwarf_armies[
    'elite'].description = 'greybeard', 'greybeards', 'Greybeards are capable of defending, as well as attacking.'
dwarf_armies['monster'].class_name, dwarf_armies['monster'].class_name_plural, dwarf_armies[
    'monster'].description = 'manticore', 'manticores', 'Manticores are incredibly powerful monsters.'

# Peasants
dwarf_armies['peasant'].category = "Infantry"
dwarf_armies['peasant'].armour_type = "Unarmoured"
# Soldiers
dwarf_armies['soldier'].category = "Infantry"
dwarf_armies['soldier'].armour_type = "Leather"
# Archers
dwarf_armies['archer'].category = "Infantry"
dwarf_armies['archer'].armour_type = "Leather"
# Besiegers
dwarf_armies['besieger'].category = "Siege"
dwarf_armies['besieger'].armour_type = "Plate"
# Elites
dwarf_armies['elite'].category = "Infantry"
dwarf_armies['elite'].armour_type = "Plate"
# Monsters
dwarf_armies['monster'].category = "Infantry"
dwarf_armies['monster'].armour_type = "Plate"

