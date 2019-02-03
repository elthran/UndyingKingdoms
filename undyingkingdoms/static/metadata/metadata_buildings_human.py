from copy import deepcopy

from undyingkingdoms.static.metadata.metadata_buildings_all import generic_buildings


human_buildings = deepcopy(generic_buildings)
# First the strings and descriptions
human_buildings['house'].class_name, human_buildings['house'].class_name_plural = 'homestead', 'homesteads'
human_buildings['field'].class_name, human_buildings['field'].class_name_plural = 'wheat field', 'wheat fields'
human_buildings['pasture'].class_name, human_buildings['pasture'].class_name_plural = 'dairy farm', 'dairy farms'
human_buildings['mill'].class_name, human_buildings['mill'].class_name_plural = 'lumber mill', 'lumber mills'
human_buildings['mine'].class_name, human_buildings['mine'].class_name_plural = 'iron mine', 'iron mines'
human_buildings['fort'].class_name, human_buildings['fort'].class_name_plural = 'palisade', 'palisades'
human_buildings['stables'].class_name, human_buildings['stables'].class_name_plural = 'stables', 'stables'
human_buildings['guild'].class_name, human_buildings['guild'].class_name_plural = 'thieves guild', 'thieves guild'
human_buildings['bank'].class_name, human_buildings['bank'].class_name_plural = 'treasury', 'treasury'

