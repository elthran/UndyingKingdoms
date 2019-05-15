from ..notifications import Notification
from utilities.helpers import to_class_name
from ..interfaces import Command


class Effect(Command):
    def __init__(self, spell, casting, caster, target):
        self.spell = spell
        self.casting = casting
        self.caster = caster
        self.target = target
        self.power = int(spell.output * caster.spell_modifier)
        # Initialize class from name. This must go after the previous lines
        self.effect_specifics = self.get_specifics()
        self.pay_cost()

    def pay_cost(self):
        self.caster.mana -= self.spell.mana_cost
        if self.spell.category == 'aura':
            self.casting.active = True

    def recoup_cost(self):
        wizardry = self.caster.wizardry
        self.caster.mana += self.spell.mana_cost * wizardry.recoup_factor

    def get_specifics(self):
        """Initialize an object from a casting name."""
        return globals()[to_class_name(self.casting.name)](self)

    def execute(self):
        if self.spell.mana_sustain > 0:
            self.casting.active = True
            self.casting.mana_sustain = self.spell.mana_sustain
        self.effect_specifics.execute()


class InitMixin:
    def __init__(self, effect):
        self.spell = effect.spell
        self.casting = effect.casting
        self.caster = effect.caster
        self.target = effect.target
        self.power = effect.power


class InstantHappiness(InitMixin, Command):
    def execute(self):
        self.caster.happiness += self.power


class InstantResearch(InitMixin, Command):
    def execute(self):
        self.caster.research += self.power


class StealGold(InitMixin, Command):
    def execute(self):
        amount = min(self.target.gold, self.power)
        self.caster.gold += amount
        self.target.gold -= amount
        notification = Notification(
            self.target,
            "Enemy magic",
            f"Enemy wizards of {self.caster.name} have convinced you to send them {amount} gold.",
            "Magic"
        )
        notification.save()


class ModifyMagicDisrupt(InitMixin, Command):
    def execute(self):
        pass


class ModifyThiefPrevention(InitMixin, Command):
    def execute(self):
        notification = Notification(
            self.target,
            "Enemy magic",
            f"Enemy wizards of {self.caster.name} have shrouded your land in darkness, "
            f"making it very difficult to catch enemy thieves.",
            "Magic"
        )
        notification.save()


class ModifyGrainRate(InitMixin, Command):
    def execute(self):
        pass


class ModifyDeathRate(InitMixin, Command):
    def execute(self):
        notification = Notification(
            self.target,
            "Enemy magic",
            f"A plague wind has been summoned by the wizards of {self.caster.name}",
            "Magic"
        )
        notification.save()


class ModifyOffensivePower(InitMixin, Command):
    def execute(self):
        pass


class ModifyBirthRate(InitMixin, Command):
    def execute(self):
        pass


class PopulationKiller(InitMixin, Command):
    def execute(self):
        kill_count = int(self.target.population * self.power / 100)
        self.target.population -= kill_count
        notification = Notification(
            self.target,
            "Enemy magic",
            f"The wizards of {self.caster.name} have cast {self.spell.display_name} on your county,"
            f" killing {kill_count} of your people.",
            "Magic"
        )
        notification.save()


class ArcherKiller(InitMixin, Command):
    def execute(self):
        kill_count = min(self.target.armies['archer'].total, self.power)
        self.target.armies['archer'].total -= kill_count
        notification = Notification(
            self.target,
            "Enemy magic",
            f"The wizards of {self.caster.name} have cast {self.spell.display_name} on your county,"
            f" killing {kill_count} of your {self.target.armies['archer'].class_name_plural}.",
            "Magic"
        )
        notification.save()


class SummonTier1(InitMixin, Command):
    def execute(self):
        self.target.armies['summon'].total += self.power


class ConvertIronToGold(InitMixin, Command):
    def execute(self):
        max_iron = min(self.caster.iron, 10)
        self.caster.iron -= max_iron
        self.caster.gold += (max_iron * self.power)


class ConvertCitizensIntoPeasants(InitMixin, Command):
    def execute(self):
        max_peasants = min(self.caster.get_available_workers(), self.power)
        self.caster.armies['peasant'].total += max_peasants
