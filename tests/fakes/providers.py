from itertools import repeat

import faker
from faker.providers import BaseProvider

from tests import bp, pp
from undyingkingdoms.blueprints.admin.metadata import bot_county_prefix, bot_county_suffix, bot_leader_prefix, \
    bot_leader_suffix
from undyingkingdoms.calculations.distributions import bell_curvish, normalize, curve_bounds
from undyingkingdoms.static.metadata.metadata import metadata_races, metadata_titles, metadata_backgrounds
from undyingkingdoms.static.metadata.research.metadata_research_all import generic_technology
from utilities.helpers import romanize

fake = faker.Faker()


# noinspection PyMethodMayBeStatic
class Provider(BaseProvider):
    def county(self):
        return fake.word(ext_word_list=bot_county_prefix) + fake.word(ext_word_list=bot_county_suffix)

    def leader(self):
        return fake.word(ext_word_list=bot_leader_prefix) + fake.word(ext_word_list=bot_leader_suffix)

    def race(self, races=None):
        if races is None:
            races = metadata_races
        return fake.word(ext_word_list=races)

    def title(self, titles=None):
        if titles is None:
            titles = metadata_titles
        return fake.word(ext_word_list=titles)

    def background(self, backgrounds=None):
        if backgrounds is None:
            backgrounds = metadata_backgrounds
        return fake.word(ext_word_list=backgrounds)

    def tech(self, technologies=None):
        if technologies is None:
            technologies = generic_technology.keys()
        return fake.word(ext_word_list=technologies)

    def requirement(self, requirements=None, nb_elements=2, variable_nb_elements=True):
        """Return a technology its associated requirement list.

        Looks like this:
        ('public works', ['engineering', 'logistics'])
        """
        if variable_nb_elements:
            nb_elements = self.randomize_nb_elements(nb_elements, min=0)

        if requirements is None:
            requirements = generic_technology.keys()

        key = self.generator.word(ext_word_list=requirements)
        value = self.generator.words(nb_elements, ext_word_list=set(requirements) - {key})

        return key, value

    def requirements(self, requirements=None, depth=6, level_1s=4, variable_nb_elements=True):
        """Return a tree of depth x with a bell curve-ish shape.

        Looks like this:
        generic_requirements = {
            'public works': [
                'engineering',
                'logistics'
            ],
        }
        """
        if requirements is None:
            requirements = generic_technology.keys()
        if variable_nb_elements:
            level_1s = self.randomize_nb_elements(level_1s, min=1)
        if depth < 3:
            raise ValueError("You can't generate a tree of less than 3 depth.")

        curve = bell_curvish(depth)
        bounds = curve_bounds(curve, requirements, level_1s)
        norms = [round(n) for n in normalize(curve, bounds)]

        req_dict = {}
        for index, layer_size in enumerate(norms):
            for _ in range(layer_size):
                # TODO: should reduce local set of requirements each execution
                key, value = self.requirement(requirements)
                # names to be 1st, 2nd, 3rd, etc.
                key = romanize(key, index)
                value = [romanize(v, index) for v in value]
                req_dict[key] = value

        return req_dict


fake.add_provider(Provider)

