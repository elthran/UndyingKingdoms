from copy import deepcopy

from app.metadata.magic.metadata_magic_all import generic_spells
from app.metadata.research.metadata_research_all import generic_technology, generic_requirements
from lib.combiners import combine_dicts
from app.virtual_classes.all_metadata_imports import all_metadata_imports as md
# TODO: refactor this module into a Heritage class. :)


def get_racial_buildings(race):
    race = race.lower()
    building_mod = md[f'metadata_buildings_{race}']
    race_buildings = getattr(building_mod, f'{race}_buildings')
    return deepcopy(race_buildings)


def add_racial_data(self):
    # Buildings and Armies extracted from metadata
    race = self.race.lower()

    armies_mod = md[f'metadata_armies_{race}']
    magic_mod = md[f'metadata_magic_{race}']
    research_mod = md[f'metadata_research_{race}']

    race_armies = getattr(armies_mod, f'{race}_armies')
    race_spells = getattr(magic_mod, f'{race}_spells')
    race_technology = getattr(research_mod, f'{race}_technology')

    self.armies = deepcopy(race_armies)
    self.magic = {**deepcopy(generic_spells), **deepcopy(race_spells)}
    self.technologies = {**deepcopy(generic_technology), **deepcopy(race_technology)}


def add_background_data(self):
    background = self.background.lower()
    magic_mod = md[f'metadata_magic_{background}']
    research_mod = md[f'metadata_research_{background}']

    background_spells = getattr(magic_mod, f'{background}_spells')
    background_technology = getattr(research_mod, f'{background}_technology')

    # Make sure tech names don't overlap.
    # This should probably be part of some fancy test suite ...
    intersection = set(self.technologies.keys()) & background_technology.keys()
    assert intersection == set(), f"Names of technologies conflict: {intersection}."

    self.magic = {**self.magic, **deepcopy(background_spells)}
    self.technologies = {**self.technologies, **deepcopy(background_technology)}


def merge_tech_requirements(race, background):
    race = race.lower()
    background = background.lower()

    race_mod = md[f'metadata_research_{race}']
    background_mod = md[f'metadata_research_{background}']

    race_reqs = {}
    background_reqs = {}
    try:
        race_reqs = getattr(race_mod, f'{race}_requirements')
    except AttributeError:
        pass

    try:
        background_reqs = getattr(background_mod, f'{background}_requirements')
    except AttributeError:
        pass

    all_requirements = combine_dicts(generic_requirements, race_reqs)
    all_requirements = combine_dicts(all_requirements, background_reqs)
    return all_requirements
