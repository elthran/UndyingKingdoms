from copy import deepcopy

from undyingkingdoms.static.metadata.buildings.metadata_buildings_all import generic_buildings


ogre_buildings = deepcopy(generic_buildings)
# First the strings and descriptions
ogre_buildings['house'].class_name, ogre_buildings['house'].class_name_plural = 'hut', 'huts'
ogre_buildings['field'].class_name, ogre_buildings['field'].class_name_plural = 'barley field', 'barley fields'
ogre_buildings['pasture'].class_name, ogre_buildings['pasture'].class_name_plural = 'dairy pasture', 'dairy pastures'
ogre_buildings['mill'].class_name, ogre_buildings['mill'].class_name_plural = 'lumber mill', 'lumber mills'
ogre_buildings['mine'].class_name, ogre_buildings['mine'].class_name_plural = 'iron mine', 'iron mines'
ogre_buildings['quarry'].class_name, ogre_buildings['quarry'].class_name_plural = 'stone quarry', 'stone quarries'
ogre_buildings['fort'].class_name, ogre_buildings['fort'].class_name_plural = 'wooden fort', 'wooden forts'
ogre_buildings['stables'].class_name, ogre_buildings['stables'].class_name_plural = 'cart factory', 'cart factories'
ogre_buildings['bank'].class_name, ogre_buildings['bank'].class_name_plural = 'vault', 'vault'
ogre_buildings['tavern'].class_name, ogre_buildings['tavern'].class_name_plural = 'thieves den', 'thieves den'
ogre_buildings['lab'].class_name, ogre_buildings['lab'].class_name_plural = 'potion shop', 'potion shops'
ogre_buildings['arcane'].class_name, ogre_buildings['arcane'].class_name_plural = 'ritual hut', 'ritual huts'
ogre_buildings['lair'].class_name, ogre_buildings['lair'].class_name_plural = 'mammoth cave', 'mammoth caves'




