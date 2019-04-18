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
        return globals()[to_class_name(self.casting.name)](self)

    def execute(self):
        if self.spell.mana_sustain > 0:
            self.casting.active = True
            self.casting.mana_sustain = self.spell.mana_sustain
        self.effect_specifics.execute()


class EffectMixin:
    def __init__(self, effect):
        self.spell = effect.spell
        self.casting = effect.casting
        self.caster = effect.caster
        self.target = effect.target


class Inspire(EffectMixin, Command):
    def execute(self):
        amount = 5 * (self.caster.buildings['arcane'].total * self.caster.buildings['arcane'].output) / 100
        self.caster.happiness += floor(amount)


class SummonGolem(EffectMixin, Command):
    def execute(self):
        pass
