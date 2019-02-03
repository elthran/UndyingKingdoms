from copy import deepcopy

from undyingkingdoms.static.metadata.metadata_all_races import generic_buildings

dwarf_buildings = deepcopy(generic_buildings)
# First the strings and descriptions
dwarf_buildings['house'].class_name, dwarf_buildings['house'].class_name_plural = 'cottage', 'cottages'
dwarf_buildings['field'].class_name, dwarf_buildings['field'].class_name_plural = 'cottage', 'cottages'
# dwarf_buildings['houses'].class_name, dwarf_buildings['houses'].class_name_plural = 'cottage', 'cottages'
# dwarf_buildings['houses'].class_name, dwarf_buildings['houses'].class_name_plural = 'cottage', 'cottages'
# dwarf_buildings['houses'].class_name, dwarf_buildings['houses'].class_name_plural = 'cottage', 'cottages'
# dwarf_buildings['houses'].class_name, dwarf_buildings['houses'].class_name_plural = 'cottage', 'cottages'
# dwarf_buildings['houses'].class_name, dwarf_buildings['houses'].class_name_plural = 'cottage', 'cottages'
# dwarf_buildings['houses'].class_name, dwarf_buildings['houses'].class_name_plural = 'cottage', 'cottages'
# dwarf_buildings['houses'].class_name, dwarf_buildings['houses'].class_name_plural = 'cottage', 'cottages'

