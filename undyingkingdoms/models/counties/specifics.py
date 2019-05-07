from copy import deepcopy

from ..magic import Magic
from undyingkingdoms.metadata.magic.metadata_magic_all import generic_spells
from undyingkingdoms.metadata.research.metadata_research_all import generic_technology
from . import all_metadata_imports as md


def add_background_data(self):
    background = self.background.lower()
    background_spells = getattr(md, f'{background}_spells')
    background_technology = getattr(md, f'{background}_technology')

    # Make sure tech names don't overlap.
    # This should probably be part of some fancy test suite ...
    intersection = set(self.technologies.keys()) & background_technology.keys()
    assert intersection == set(), f"Names of technologies conflict: {intersection}."

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
