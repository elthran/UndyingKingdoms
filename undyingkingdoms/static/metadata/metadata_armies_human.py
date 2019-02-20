from copy import deepcopy

from undyingkingdoms.static.metadata.metadata_armies_all import generic_armies

human_armies = deepcopy(generic_armies)
# First the strings and descriptions
human_armies['peasant'].class_name, human_armies['peasant'].class_name_plural, human_armies[
    'peasant'].description = 'man-at-arms', 'men-at-arms', 'Men-at-arms can be trained extremely quickly and have low upkeep.'
human_armies['soldier'].class_name, human_armies['soldier'].class_name_plural, human_armies[
    'soldier'].description = 'footman', 'footmen', 'Footmen are strong attackers.'
human_armies['archer'].class_name, human_armies['archer'].class_name_plural, human_armies[
    'archer'].description = 'musketeer', 'musketeers', 'Crossbowmen are excellent at defending.'
human_armies['elite'].class_name, human_armies['elite'].class_name_plural, human_armies[
    'elite'].description = 'knight', 'knights', 'Knights are one of the best attackers.'
human_armies['monster'].class_name, human_armies['monster'].class_name_plural, human_armies[
    'monster'].description = 'gryphon', 'gryphons', 'Gryphons are incredibly powerful monsters.'
# Humans: Slightly faster training and lower iron costs
# Peasants
human_armies['peasant'].trainable_per_day += 25
human_armies['peasant'].gold -= 3
human_armies['peasant'].iron -= 1
human_armies['peasant'].attack -= 1
# Soldiers
human_armies['soldier'].trainable_per_day += 5
human_armies['soldier'].iron -= 1
# Archers
human_armies['archer'].trainable_per_day += 5
human_armies['archer'].iron -= 1
# Elites
human_armies['elite'].trainable_per_day += 3
human_armies['elite'].iron -= 1
