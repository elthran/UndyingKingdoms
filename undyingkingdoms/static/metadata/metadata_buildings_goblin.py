from copy import deepcopy

from undyingkingdoms.static.metadata.metadata_all_races import generic_buildings

goblin_buildings = deepcopy(generic_buildings)
# First the strings and descriptions
goblin_buildings['house'].class_name, goblin_buildings['house'].class_name_plural = 'hovel', 'hovels'
goblin_buildings['field'].class_name, goblin_buildings['field'].class_name_plural = 'grain field', 'grain fields'
goblin_buildings['pasture'].class_name, goblin_buildings['pasture'].class_name_plural = 'sheep farm', 'sheep farms'
goblin_buildings['mill'].class_name, goblin_buildings['mill'].class_name_plural = 'lumber mill', 'lumber mills'
goblin_buildings['mine'].class_name, goblin_buildings['mine'].class_name_plural = 'iron mine', 'iron mines'
goblin_buildings['fort'].class_name, goblin_buildings['fort'].class_name_plural = 'bulwark', 'bulwarks'
goblin_buildings['stables'].class_name, goblin_buildings['stables'].class_name_plural = 'wolf kennel', 'wolf kennels'
goblin_buildings['guild'].class_name, goblin_buildings['guild'].class_name_plural = 'hideout', 'hideouts'
goblin_buildings['bank'].class_name, goblin_buildings['bank'].class_name_plural = 'storehouse', 'storehouses'

