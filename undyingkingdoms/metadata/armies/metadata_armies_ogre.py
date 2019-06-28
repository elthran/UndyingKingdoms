from copy import deepcopy

from undyingkingdoms.metadata.armies.metadata_armies_all import generic_armies

ogre_armies = deepcopy(generic_armies)
# First the strings and descriptions
ogre_armies['peasant'].attack += 1
ogre_armies['peasant'].health += 1
ogre_armies['peasant'].class_name = 'brute'
ogre_armies['peasant'].class_name_plural = 'brutes'
ogre_armies['peasant'].description = 'They excel at repelling enemy armies.'

ogre_armies['soldier'].attack += 1
ogre_armies['soldier'].health += 2
ogre_armies['soldier'].class_name = 'enforcer'
ogre_armies['soldier'].class_name_plural = 'enforcers'
ogre_armies['soldier'].description = 'Excellent offensive troops.'

ogre_armies['archer'].health += 2
ogre_armies['archer'].class_name = 'rock hurler'
ogre_armies['archer'].class_name_plural = 'rock hurlers'
ogre_armies['archer'].description = 'Very effective at defending your county.'

ogre_armies['besieger'].class_name = 'catapult'
ogre_armies['besieger'].class_name_plural = 'catapults'
ogre_armies['besieger'].description = 'Catapults are incredibly effective at attacking fortified counties.'

ogre_armies['elite'].attack += 1
ogre_armies['elite'].health += 3
ogre_armies['elite'].class_name = 'veteran'
ogre_armies['elite'].class_name_plural = 'veterans'
ogre_armies['elite'].description = 'Veterans are elite cavalry and incredibly adept at attacking enemy counties.'

ogre_armies['monster'].class_name = 'mammoth'
ogre_armies['monster'].class_name_plural = 'mammoths'
ogre_armies['monster'].description = 'Mammoths are incredibly powerful monsters.'

# Ogres: Slightly more damage and wood
# Peasants
ogre_armies['peasant'].category = "Infantry"
ogre_armies['peasant'].armour_type = "Unarmoured"
# Soldiers
ogre_armies['soldier'].category = "Infantry"
ogre_armies['soldier'].armour_type = "Leather"
# Archers
ogre_armies['archer'].category = "Infantry"
ogre_armies['archer'].armour_type = "Unarmoured"
# Besiegers
ogre_armies['besieger'].category = "Siege"
ogre_armies['besieger'].armour_type = "Plate"
# Elites
ogre_armies['elite'].category = "Infantry"
ogre_armies['elite'].armour_type = "Plate"
# Monsters
ogre_armies['monster'].category = "Monster"
ogre_armies['monster'].armour_type = "Unarmoured"
ogre_armies['monster'].ability = "Thundering Charge"
ogre_armies['monster'].ability_description = f"When attacking, each {ogre_armies['monster'].class_name}" \
    f" destroys a random enemy building."
