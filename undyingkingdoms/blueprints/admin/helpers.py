from random import choice
from uuid import uuid4

from flask import jsonify, current_app, render_template_string, url_for
from flask_login import current_user

from undyingkingdoms.controler.initialize import initialize_county
from undyingkingdoms.models.exports import World
from undyingkingdoms.utilities.convert_metadata import build_race_table, build_modifier_table
from .metadata import bot_county_prefix, bot_county_suffix, bot_leader_prefix, bot_leader_suffix
from undyingkingdoms.models.exports import Notification
from undyingkingdoms.models.exports import County
from undyingkingdoms.models.exports import User
from undyingkingdoms.models.exports import Kingdom


def create_bots(n=1):
    kingdoms = Kingdom.query.all()
    kingdoms = [  # filter out empty kingdoms
        kingdom
        for kingdom in kingdoms
        if kingdom.counties
    ]

    try:
        for i in range(n):
            smallest_kingdom = min(kingdoms, key=lambda x: len(x.counties))
            bot_name = uuid4()
            user = User(f"bot_{bot_name}",
                        f"bot_{bot_name}@gmail.com",
                        "1234")
            user.is_bot = True
            county = initialize_county(
                user, smallest_kingdom,
                f"{choice(bot_county_prefix)}{choice(bot_county_suffix)}",
                choice(["Sir", "Lady"]),
                f"{choice(bot_leader_prefix)}{choice(bot_leader_suffix)}",
                choice(["Human", "Elf", "Dwarf", "Goblin"]),
                choice(["Alchemist", "Warlord", "Rogue", "Merchant", "Wizard"])
            )
            county.save()
    except Exception as ex:
        return jsonify(
            status='fail',
            message=f"Bot creation failed due to: {ex}"
        )
    bot_plural = 'bots' if n == 1 else 'bot'
    return jsonify(
        status="success",
        message=f"Successfully create {n} {bot_plural}."
    )


def create_notification(message):
    admin_leader = current_user.county.leader
    admin_pm_url = url_for('enemy_overview', county_id=current_user.id)
    title = f'Admin Update from <a href="{admin_pm_url}">{admin_leader}</a>'
    for county in County.query.all():
        notification = Notification(
            county,
            title,
            message,
            "Admin"
        )
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
        if current_app.config['ENV'] != 'production':
            raise ex
        return jsonify(
            status='fail',
            message=f'Advance day failed due to: {ex}'
        )
