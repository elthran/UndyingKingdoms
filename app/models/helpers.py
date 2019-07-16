import functools
import os
import random

SEED_SIZE = 5


def get_max_random_int():
    random.seed(os.urandom(SEED_SIZE))
    return random.randint(-2147483648, 2147483647)


def cached_random(func):
    @functools.wraps(func)
    def wrapper(that, *args, **kwargs):
        """Wrap an object's method, allowing access to self.

        Wrapped method's self attribute can be accessed through 'that'
        parameter.

        Requires: Object to have a 'seed' parameter.

        Means you can do:

        class Foo:
            @property
            def seed(self):
                return 42

            @cached_random
            def bar(self, prediction=True):
                pass

        and 'that' will refer to Foo's self parameter.
        Foo must have a 'seed' property of some kind.
        """
        # restore cached seed to allow repeatable randoms
        if 'prediction' in kwargs and kwargs['prediction']:
            random.seed(that.seed)
        return func(that, *args, **kwargs)

    # unset random seed, currently unnecessary
    # random.seed(os.urandom(SEED_SIZE))
    return wrapper


def get_target_relation(county, target):
    """Return the relationship between two counties.

    This will get more complex over time and should be optimized.
    """
    kingdom = county.kingdom
    target_kingdom = target.kingdom
    if county == target:
        target_relation = 'self'
    elif target_kingdom in kingdom.allies:
        target_relation = 'friendly'
    elif target_kingdom in kingdom.kingdoms_in_armistice:
        target_relation = 'armistice'
    else:
        target_relation = 'hostile'

    # elif target_county.kingdom in county.kingdom.enemies:
    #     targets = 'hostile'
    # else:
    #     targets = 'all'
    # (spell.targets == 'self' and target != county) or
    # (spell.targets == 'friendly' and target.kingdom in county.kingdom.enemies) or
    # (spell.targets == 'hostile' and target.kingdom in county.kingdom.allies) or
    # (spell.targets == 'hostile' and target == county)

    return target_relation


def extract_modifiers(metadata, race, background):
    return metadata.get(race, ('', 0))[1] + metadata.get(background, ('', 0))[1]
