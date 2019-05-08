from abc import ABC, abstractmethod


class Command(ABC):
    @abstractmethod
    def execute(self):
        pass


class EffectInterface(ABC):
    @abstractmethod
    def activate(self, county):
        pass

    @abstractmethod
    def undo(self, county):
        pass
