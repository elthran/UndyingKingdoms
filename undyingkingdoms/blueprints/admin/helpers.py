from random import choice
from uuid import uuid4

from flask import jsonify

from .metadata import bot_county_prefix, bot_county_suffix, bot_leader_prefix, bot_leader_suffix
from undyingkingdoms.models.counties import County
from undyingkingdoms.models.users import User
from undyingkingdoms.models.kingdoms import Kingdom

def create_bots(n=3):
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
            choice(["Human", "Elf", "Dwarf"]),
            choice(["Sir", "Lady"]),
            choice(["Engineer", "Warlord", "Rogue", "Merchant"]))
        county.save()
        county.vote = county.id
    return jsonify(
        status="succes",
        message=f"Successfully create {n} bots."
    )
