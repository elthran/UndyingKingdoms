from copy import deepcopy

from undyingkingdoms.static.metadata.metadata_buildings_all import generic_buildings


elf_buildings = deepcopy(generic_buildings)
# First the strings and descriptions
elf_buildings['house'].class_name, elf_buildings['house'].class_name_plural = 'sanctuary', 'sanctuaries'
elf_buildings['field'].class_name, elf_buildings['field'].class_name_plural = 'rice field', 'rice fields'
elf_buildings['pasture'].class_name, elf_buildings['pasture'].class_name_plural = 'dairy pasture', 'dairy pastures'
elf_buildings['mill'].class_name, elf_buildings['mill'].class_name_plural = 'lumber mill', 'lumber mills'
elf_buildings['mine'].class_name, elf_buildings['mine'].class_name_plural = 'iron mine', 'iron mines'
elf_buildings['fort'].class_name, elf_buildings['fort'].class_name_plural = 'citadel', 'citadels'
elf_buildings['stables'].class_name, elf_buildings['stables'].class_name_plural = 'elk stables', 'elk stables'
elf_buildings['guild'].class_name, elf_buildings['guild'].class_name_plural = 'thieves guild', 'thieves guilds'
elf_buildings['bank'].class_name, elf_buildings['bank'].class_name_plural = 'exchequer', 'exchequers'
elf_buildings['lair'].class_name, elf_buildings['lair'].class_name_plural = 'dragon den', 'dragon dens'
# Goblins:
elf_buildings['stables'].output += 1
elf_buildings['stables'].stone_cost += 5


