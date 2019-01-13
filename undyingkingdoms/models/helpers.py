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
        as long as Foo also has a 'seed' property of some kind.
        """
        # restore cached seed to allow repeatable randoms
        if 'prediction' in kwargs and kwargs['prediction']:
            random.seed(that.seed)
        return func(that, *args, **kwargs)

    # unset random seed, currently unnecessary
    # random.seed(os.urandom(SEED_SIZE))
    return wrapper
