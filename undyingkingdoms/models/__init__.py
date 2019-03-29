from .users import User
from .counties import County
from .buildings import Building
from .armies import Army
from .kingdoms import Kingdom
from .sessions import Session
from .notifications import Notification
from .achievements import Achievement
from .dau import DAU
from .worlds import World
from .transactions import Transaction
from .expeditions import Expedition
from .infiltrations import Infiltration
from .upvotes import Upvote
from .chatroom import Chatroom
from .messages import Message
from .diplomacy import Diplomacy
from .magic import Magic
from .casting import Casting
from .clans import Clan


# Allows adding relationships that can't be declared in class
# due to buggy import loop.
from undyingkingdoms.models.bases import db
Army.county = db.relationship('County')
User.county = db.relationship('County', backref='user', uselist=False)
Casting.caster = db.relationship('County', foreign_keys="[Casting.county_id]")


# Attach any addons with multiple participants.
from .addons.clan_addon import clan_addon
clan_addon(User, Clan, Kingdom)

Infiltration.target = db.relationship('County', foreign_keys="[Infiltration.target_id]")

