from random import choice
from uuid import uuid4

from flask import jsonify

from undyingkingdoms import User
from undyingkingdoms.blueprints.admin.metadata import bot_county_prefix, bot_county_suffix, bot_leader_prefix, \
    bot_leader_suffix
from undyingkingdoms.controler.initialize import initialize_county
from undyingkingdoms.models.kingdoms import Kingdom


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
