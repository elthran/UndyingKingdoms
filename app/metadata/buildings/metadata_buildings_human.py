from copy import deepcopy

from app.metadata.buildings.metadata_buildings_all import generic_buildings


human_buildings = deepcopy(generic_buildings)
# First the strings and descriptions
human_buildings['house'].class_name, human_buildings['house'].class_name_plural = 'homestead', 'homesteads'
human_buildings['field'].class_name, human_buildings['field'].class_name_plural = 'wheat field', 'wheat fields'
human_buildings['pasture'].class_name, human_buildings['pasture'].class_name_plural = 'dairy farm', 'dairy farms'
human_buildings['mill'].class_name, human_buildings['mill'].class_name_plural = 'lumber mill', 'lumber mills'
human_buildings['mine'].class_name, human_buildings['mine'].class_name_plural = 'iron mine', 'iron mines'
human_buildings['quarry'].class_name, human_buildings['quarry'].class_name_plural = 'stone quarry', 'stone quarries'
human_buildings['fort'].class_name, human_buildings['fort'].class_name_plural = 'palisade', 'palisades'
human_buildings['stables'].class_name, human_buildings['stables'].class_name_plural = 'stables', 'stables'
human_buildings['bank'].class_name, human_buildings['bank'].class_name_plural = 'treasury', 'treasury'
human_buildings['tavern'].class_name, human_buildings['tavern'].class_name_plural = 'thieves tavern', 'thieves tavern'
human_buildings['lab'].class_name, human_buildings['lab'].class_name_plural = 'workshop', 'workshops'
human_buildings['arcane'].class_name, human_buildings['arcane'].class_name_plural = 'college of magic', 'colleges of magic'
human_buildings['lair'].class_name, human_buildings['lair'].class_name_plural = 'gryphon aviary', 'gryphon aviaries'


