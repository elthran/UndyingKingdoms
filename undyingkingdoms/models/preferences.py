import math
from datetime import datetime, timedelta
from random import choice, uniform, randint

from sqlalchemy import desc
from sqlalchemy.orm.collections import attribute_mapped_collection

from undyingkingdoms.models.bases import GameState, db
from undyingkingdoms.models.helpers import cached_random
from undyingkingdoms.models.notifications import Notification
from undyingkingdoms.models.expeditions import Expedition
from undyingkingdoms.models.infiltrations import Infiltration
from undyingkingdoms.models.trades import Trade
from undyingkingdoms.static.metadata.metadata import birth_rate_modifier, food_consumed_modifier, death_rate_modifier, \
    income_modifier, production_per_worker_modifier, offensive_power_modifier, defense_per_citizen_modifier, \
    happiness_modifier, buildings_built_per_day_modifier

from copy import deepcopy

from undyingkingdoms.static.metadata.metadata_armies_dwarf import dwarf_armies
from undyingkingdoms.static.metadata.metadata_armies_elf import elf_armies
from undyingkingdoms.static.metadata.metadata_armies_goblin import goblin_armies
from undyingkingdoms.static.metadata.metadata_armies_human import human_armies
from undyingkingdoms.static.metadata.metadata_buildings_dwarf import dwarf_buildings
from undyingkingdoms.static.metadata.metadata_buildings_elf import elf_buildings
from undyingkingdoms.static.metadata.metadata_buildings_goblin import goblin_buildings
from undyingkingdoms.static.metadata.metadata_buildings_human import human_buildings
from undyingkingdoms.static.metadata.metadata_research_all import generic_technology


class Preferences(GameState):
    county_id = db.Column(db.Integer, db.ForeignKey('county.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    tax_rate = db.Column(db.Integer)
    rations = db.Column(db.Integer)
    production_choice = db.Column(db.Integer)
    research = db.Column(db.String(128))

    def __init__(self, county_id, user_id):
        self.county_id = county_id
        self.user_id = user_id
        self.tax_rate = 5
        self.rations = 1
        self.production_choice = 0
