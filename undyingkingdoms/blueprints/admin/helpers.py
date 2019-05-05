from random import choice
from uuid import uuid4

from flask import jsonify
from flask_login import current_user

from undyingkingdoms.models.exports import World
from undyingkingdoms.models.exports import Preferences
from undyingkingdoms.utilities.convert_metadata import build_race_table, build_modifier_table
from .metadata import bot_county_prefix, bot_county_suffix, bot_leader_prefix, bot_leader_suffix
from undyingkingdoms.models.exports import Notification
from undyingkingdoms.models.exports import County
from undyingkingdoms.models.exports import User
from undyingkingdoms.models.exports import Kingdom


def create_bots(n=1):
    kingdoms = Kingdom.query.all()

    for i in range(n):
        smallest_kingdom = min(kingdoms, key=lambda x: len(x.counties))
        bot_name = uuid4()
        user = User(f"bot_{bot_name}",
                    f"bot_{bot_name}@gmail.com",
                    "1234")
        user.is_bot = True
        user.save()
        county = County(
            smallest_kingdom.id,
            f"{choice(bot_county_prefix)}{choice(bot_county_suffix)}",
            f"{choice(bot_leader_prefix)}{choice(bot_leader_suffix)}",
            user.id,
            choice(["Human", "Elf", "Dwarf", "Goblin"]),
            choice(["Sir", "Lady"]),
            choice(["Alchemist", "Warlord", "Rogue", "Merchant", "Wizard"]))
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
        notification = Notification(county.id,
                                    f"Admin Update from {current_user.county.leader}",
                                    message,
                                    world.day,
                                    "Admin")
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
