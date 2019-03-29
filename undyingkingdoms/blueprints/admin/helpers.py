from random import choice
from uuid import uuid4

from flask import jsonify
from flask_login import current_user

from undyingkingdoms.models import World
from undyingkingdoms.models.preferences import Preferences
from undyingkingdoms.utilities.convert_metadata import build_race_table, build_modifier_table
from .metadata import bot_county_prefix, bot_county_suffix, bot_leader_prefix, bot_leader_suffix
from undyingkingdoms.models.notifications import Notification
from undyingkingdoms.models.counties import County
from undyingkingdoms.models.users import User
from undyingkingdoms.models.kingdoms import Kingdom


def create_bots(n=1):
    kingdoms = Kingdom.query.all()

    for i in range(n):
        smallest_kingdom = min(kingdoms, key=lambda x: len(x.counties))
        bot_name = uuid4()
        user = User("bot_{}".format(bot_name),
                    "bot_{}@gmail.com".format(bot_name),
                    "1234")
        user.is_bot = True
        user.save()
        county = County(
            smallest_kingdom.id, "{}{}".format(
                choice(bot_county_prefix),
                choice(bot_county_suffix)),
            "{}{}".format(
                choice(bot_leader_prefix),
                choice(bot_leader_suffix)),
            user.id,
            choice(["Human", "Elf", "Dwarf", "Goblin"]),
            choice(["Sir", "Lady"]),
            choice(["Engineer", "Warlord", "Rogue", "Merchant"]))
        county.save()
        county.vote = county.id
        preferences = Preferences(county.id, county.user.id)
        preferences.save()
    return jsonify(
        status="success",
        message=f"Successfully create {n} bots."
    )


def create_notification(message):
    world = World.query.first()
    for county in County.query.all():
        notification = Notification(county.id, "Admin Update from {}".format(current_user.county.leader), message, world.day, "Admin")
        notification.save()
    return jsonify(
        status="success",
        message=f"Successfully sent notice '{message}' to all active users."
    )


def build_comparison_files():
    """Build nice spreadsheets from python metadata dictionaries."""

    try:
        build_race_table()
        build_modifier_table()
        return jsonify(
            status="success",
            message="You successfully updated the comparison tables for the player guide."
        )
    except Exception as ex:
        return jsonify(
            status="fail",
            message=f"Player guide update failed due to: {ex}"
        )

def run_advance_day():
    try:
        world = World.query.first()
        world.advance_day()
        return jsonify(
            status='success',
            message='You successfully advanced the game world one day.'
        )
    except Exception as ex:
        return jsonify(
            status='fail',
            message=f'Advance day failed due to: {ex}'
        )
