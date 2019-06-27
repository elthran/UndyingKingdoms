from copy import deepcopy

from undyingkingdoms.metadata.armies.metadata_armies_all import generic_armies

human_armies = deepcopy(generic_armies)
# First the strings and descriptions
human_armies['peasant'].class_name, human_armies['peasant'].class_name_plural, human_armies[
    'peasant'].description = 'man-at-arms', 'men-at-arms', 'Men-at-arms can be trained extremely quickly and have low upkeep.'
human_armies['soldier'].class_name, human_armies['soldier'].class_name_plural, human_armies[
    'soldier'].description = 'footman', 'footmen', 'Footmen are strong attackers.'
human_armies['archer'].class_name, human_armies['archer'].class_name_plural, human_armies[
    'archer'].description = 'musketeer', 'musketeers', 'Musketeers are excellent at defending.'
human_armies['besieger'].class_name, human_armies['besieger'].class_name_plural, human_armies[
    'besieger'].description = 'trebuchet', 'trebuchets', 'Trebuchets are incredibly effective against fortified counties.'
human_armies['elite'].class_name, human_armies['elite'].class_name_plural, human_armies[
    'elite'].description = 'knight', 'knights', 'Knights are one of the best attackers.'
human_armies['monster'].class_name, human_armies['monster'].class_name_plural, human_armies[
    'monster'].description = 'gryphon', 'gryphons', 'Gryphons are incredibly powerful monsters.'
# Humans: Slightly faster training and lower iron costs
# Peasants
human_armies['peasant'].category = "Infantry"
human_armies['peasant'].armour_type = "Unarmoured"
# Soldiers
human_armies['soldier'].category = "Infantry"
human_armies['soldier'].armour_type = "Leather"
# Archers
human_armies['archer'].category = "Infantry"
human_armies['archer'].armour_type = "Leather"
# Besiegers
human_armies['besieger'].category = "Siege"
human_armies['besieger'].armour_type = "Plate"
# Elites
human_armies['elite'].category = "Cavalry"
human_armies['elite'].armour_type = "Plate"
# Monsters
human_armies['monster'].category = "Monster"
human_armies['monster'].armour_type = "Plate"
human_armies['monster'].ability = "Inspiring Presence"
human_armies['monster'].ability_description = "When attacking, your entire army gains +1% power."
