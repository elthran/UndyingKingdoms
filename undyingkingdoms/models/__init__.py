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
from .magic import Casting
from .clans import Clan
from .preferences import Preferences
from .technologies import Technology


# Allows adding relationships that can't be declared in class
# due to buggy import loop.
from undyingkingdoms.models.bases import db
Army.county = db.relationship('County')
User.county = db.relationship('County', backref='user', uselist=False)
Casting.caster = db.relationship('County', foreign_keys="[Casting.county_id]")
User.preferences = db.relationship("Preferences", back_populates="user", uselist=False)
Preferences.county = db.relationship("County", back_populates='preferences', foreign_keys="Preferences.county_id")
Preferences.vote = db.relationship("County", foreign_keys="Preferences.vote_id")
Infiltration.target = db.relationship('County', foreign_keys="[Infiltration.target_id]")


# Attach any addons with multiple participants.
from .addons.clan_addon import clan_addon
from undyingkingdoms.models.addons.tech_addons import completed_techs_addon, incomplete_techs_addon, \
    available_techs_addon, advance_research_addon, establish_requirements_init_addon

clan_addon(User, Clan, Kingdom)
completed_techs_addon(County)
incomplete_techs_addon(County)
available_techs_addon(County)
advance_research_addon(County)


