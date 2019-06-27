from copy import deepcopy

from undyingkingdoms.metadata.armies.metadata_armies_all import generic_armies

elf_armies = deepcopy(generic_armies)
# First the strings and descriptions
elf_armies['peasant'].class_name, elf_armies['peasant'].class_name_plural, elf_armies[
    'peasant'].description = 'defender', 'defenders', 'They excel at repelling enemy armies.'
elf_armies['soldier'].class_name, elf_armies['soldier'].class_name_plural, elf_armies[
    'soldier'].description = 'ranger', 'rangers', 'Excellent offensive troops.'
elf_armies['archer'].class_name, elf_armies['archer'].class_name_plural, elf_armies[
    'archer'].description = 'longbowman', 'longbowmen', 'Longbowmen are very effective at defending your county.'
elf_armies['besieger'].class_name, elf_armies['besieger'].class_name_plural, elf_armies[
    'besieger'].description = 'Balista', 'Balistae', 'Balistae are incredibly effective at attacking fortified counties.'
elf_armies['elite'].class_name, elf_armies['elite'].class_name_plural, elf_armies[
    'elite'].description = 'dragonhelm', 'dragonhelms', 'Dragonhelms are elite cavalry and incredibly adept at attacking enemy counties.'
elf_armies['monster'].class_name, elf_armies['monster'].class_name_plural, elf_armies[
    'monster'].description = 'phoenix', 'phoenixes', 'Phoenixes are incredibly powerful monsters.'
# Elves: Slightly more damage and wood
# Peasants
elf_armies['peasant'].category = "Infantry"
elf_armies['peasant'].armour_type = "Unarmoured"
# Soldiers
elf_armies['soldier'].category = "Infantry"
elf_armies['soldier'].armour_type = "Leather"
# Archers
elf_armies['archer'].category = "Infantry"
elf_armies['archer'].armour_type = "Leather"
# Besiegers
elf_armies['besieger'].category = "Siege"
elf_armies['besieger'].armour_type = "Plate"
# Elites
elf_armies['elite'].category = "Cavalry"
elf_armies['elite'].armour_type = "Plate"
# Monsters
elf_armies['monster'].category = "Monster"
elf_armies['monster'].armour_type = "Plate"
elf_armies['monster'].ability = "Rebirth"
elf_armies['monster'].ability_description = f"After any battle, each dead {elf_armies['monster'].class_name} " \
                                            f"has a 50% chance to come back to life."
