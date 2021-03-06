from copy import deepcopy

from app.metadata.buildings.metadata_buildings_all import generic_buildings

goblin_buildings = deepcopy(generic_buildings)
# First the strings and descriptions
goblin_buildings['house'].class_name, goblin_buildings['house'].class_name_plural = 'hovel', 'hovels'
goblin_buildings['field'].class_name, goblin_buildings['field'].class_name_plural = 'grain field', 'grain fields'
goblin_buildings['pasture'].class_name, goblin_buildings['pasture'].class_name_plural = 'sheep farm', 'sheep farms'
goblin_buildings['mill'].class_name, goblin_buildings['mill'].class_name_plural = 'lumber mill', 'lumber mills'
goblin_buildings['mine'].class_name, goblin_buildings['mine'].class_name_plural = 'iron mine', 'iron mines'
goblin_buildings['quarry'].class_name, goblin_buildings['quarry'].class_name_plural = 'stone quarry', 'stone quarries'
goblin_buildings['fort'].class_name, goblin_buildings['fort'].class_name_plural = 'bulwark', 'bulwarks'
goblin_buildings['stables'].class_name, goblin_buildings['stables'].class_name_plural = 'wolf kennel', 'wolf kennels'
goblin_buildings['bank'].class_name, goblin_buildings['bank'].class_name_plural = 'storehouse', 'storehouses'
goblin_buildings['tavern'].class_name, goblin_buildings['tavern'].class_name_plural = 'hideout', 'hideouts'
goblin_buildings['lab'].class_name, goblin_buildings['lab'].class_name_plural = 'foundry', 'foundries'
goblin_buildings['arcane'].class_name, goblin_buildings['arcane'].class_name_plural = 'witch hut', 'witch huts'
goblin_buildings['lair'].class_name, goblin_buildings['lair'].class_name_plural = 'wyvern lair', 'wyvern lairs'
