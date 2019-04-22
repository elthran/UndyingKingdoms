from math import floor

from utilities.helpers import to_class_name
from .interface import Command


class Effect(Command):
    def __init__(self, spell, casting, caster, target):
        self.spell = spell
        self.casting = casting
        self.caster = caster
        self.target = target
        # initialize class from name.
        self.effect_specifics = self.get_specifics()
        self.pay_cost()

    def pay_cost(self):
        self.caster.mana -= self.spell.mana_cost
        if self.spell.category == 'aura':
            self.casting.active = True

    def get_specifics(self):
        """Initialize an object from a casting name."""
        print("STUFFFFF:", self.casting.name)
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


class Inspire(InitMixin, Command):
    def execute(self):
        amount = 5 * (self.caster.buildings['arcane'].total * self.caster.buildings['arcane'].output) / 100
        self.caster.happiness += floor(amount)


class SummonGolem(InitMixin, Command):
    def execute(self):
        pass


class SecretsOfAlchemy(InitMixin, Command):
    def execute(self):
        max_iron = min(self.caster.iron, 10)
        self.caster.iron -= max_iron
        self.caster.gold += floor(max_iron * 10 * (1 + self.caster.buildings['arcane'].total * self.caster.buildings['arcane'].output / 100))
