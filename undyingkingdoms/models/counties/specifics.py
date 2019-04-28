from copy import deepcopy

from undyingkingdoms.static.metadata.armies.metadata_armies_dwarf import dwarf_armies
from undyingkingdoms.static.metadata.armies.metadata_armies_elf import elf_armies
from undyingkingdoms.static.metadata.armies.metadata_armies_goblin import goblin_armies
from undyingkingdoms.static.metadata.armies.metadata_armies_human import human_armies
from undyingkingdoms.static.metadata.armies.metadata_armies_ogre import ogre_armies
from undyingkingdoms.static.metadata.buildings.metadata_buildings_dwarf import dwarf_buildings
from undyingkingdoms.static.metadata.buildings.metadata_buildings_elf import elf_buildings
from undyingkingdoms.static.metadata.buildings.metadata_buildings_goblin import goblin_buildings
from undyingkingdoms.static.metadata.buildings.metadata_buildings_human import human_buildings
from undyingkingdoms.static.metadata.buildings.metadata_buildings_ogre import ogre_buildings
from undyingkingdoms.static.metadata.magic.metadata_magic_all import generic_spells
from undyingkingdoms.static.metadata.magic.metadata_magic_dwarf import dwarf_spells
from undyingkingdoms.static.metadata.magic.metadata_magic_elf import elf_spells
from undyingkingdoms.static.metadata.magic.metadata_magic_goblin import goblin_spells
from undyingkingdoms.static.metadata.magic.metadata_magic_human import human_spells
from undyingkingdoms.static.metadata.magic.metadata_magic_ogre import ogre_spells
from undyingkingdoms.static.metadata.research.metadata_research_all import generic_technology
from undyingkingdoms.static.metadata.research.metadata_research_dwarf import dwarf_technology
from undyingkingdoms.static.metadata.research.metadata_research_elf import elf_technology
from undyingkingdoms.static.metadata.research.metadata_research_goblin import goblin_technology
from undyingkingdoms.static.metadata.research.metadata_research_human import human_technology
from undyingkingdoms.static.metadata.research.metadata_research_ogre import ogre_technology

from . import all_metadata_imports as md


def add_background_data(self):
    background = self.background.lower()
    background_spells = getattr(md, f'{background}_spells')
    background_technology = getattr(md, f'{background}_technology')

    self.magic = {**self.magic, **deepcopy(background_spells)}
    self.technologies = {**self.technologies, **deepcopy(background_technology)}

    if self.background == "Alchemist":
        self.buildings["lab"].output *= 2


def add_racial_data(self):
    # Buildings and Armies extracted from metadata
    race = self.race.lower()
    race_buildings = getattr(md, f'{race}_buildings')
    race_armies = getattr(md, f'{race}_armies')
    race_spells = getattr(md, f'{race}_spells')
    race_technology = getattr(md, f'{race}_technology')

    self.buildings = deepcopy(race_buildings)
    self.armies = deepcopy(race_armies)
    self.magic = {**deepcopy(generic_spells), **deepcopy(race_spells)}
    self.technologies = {**deepcopy(generic_technology), **deepcopy(race_technology)}
