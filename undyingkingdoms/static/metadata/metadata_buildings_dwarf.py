from copy import deepcopy

from undyingkingdoms.static.metadata.metadata_buildings_all import generic_buildings

dwarf_buildings = deepcopy(generic_buildings)
# First the strings and descriptions
dwarf_buildings['house'].class_name, dwarf_buildings['house'].class_name_plural = 'cottage', 'cottages'
dwarf_buildings['field'].class_name, dwarf_buildings['field'].class_name_plural = 'rye field', 'rye fields'
dwarf_buildings['pasture'].class_name, dwarf_buildings['pasture'].class_name_plural = 'goat farm', 'goat farms'
dwarf_buildings['mill'].class_name, dwarf_buildings['mill'].class_name_plural = 'lumber mill', 'lumber mills'
dwarf_buildings['mine'].class_name, dwarf_buildings['mine'].class_name_plural = 'iron mine', 'iron mines'
dwarf_buildings['quarry'].class_name, dwarf_buildings['quarry'].class_name_plural = 'stone quarry', 'stone quarries'
dwarf_buildings['fort'].class_name, dwarf_buildings['fort'].class_name_plural = 'stronghold', 'strongholds'
dwarf_buildings['stables'].class_name, dwarf_buildings['stables'].class_name_plural = 'pony stables', 'pony stables'
dwarf_buildings['bank'].class_name, dwarf_buildings['bank'].class_name_plural = 'vault', 'vaults'
dwarf_buildings['tavern'].class_name, dwarf_buildings['tavern'].class_name_plural = 'thieves den', 'thieves dens'
dwarf_buildings['lab'].class_name, dwarf_buildings['lab'].class_name_plural = 'alchemist lab', 'alchemist labs'
dwarf_buildings['arcane'].class_name, dwarf_buildings['arcane'].class_name_plural = 'rune forge', 'rune forges'
dwarf_buildings['lair'].class_name, dwarf_buildings['lair'].class_name_plural = 'manticore lair', 'manticore lairs'
# Dwarves:
dwarf_buildings['fort'].output += 2
dwarf_buildings['fort'].stone_cost += 5
dwarf_buildings['fort'].description = 'Each stronghold adds +9% to your county\'s defence value.'

dwarf_buildings['mine'].output += 1
dwarf_buildings['mine'].description = 'Each iron mine produces 3 iron a day.'
