from itertools import repeat

import faker
from faker.providers import BaseProvider

from tests import bp
from undyingkingdoms.blueprints.admin.metadata import bot_county_prefix, bot_county_suffix, bot_leader_prefix, \
    bot_leader_suffix
from undyingkingdoms.static.metadata.metadata import metadata_races, metadata_titles, metadata_backgrounds
from undyingkingdoms.static.metadata.metadata_research_all import generic_technology

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

    def requirement(self, ext_word_list=None, nb_elements=2, variable_nb_elements=True):
        """Looks like this:

        ('public works', ['engineering', 'logistics'])
        """
        if variable_nb_elements:
            nb_elements = self.randomize_nb_elements(nb_elements, min=0)

        if ext_word_list is None:
            ext_word_list = generic_technology.keys()

        key = self.generator.word(ext_word_list=ext_word_list)
        value = self.generator.words(nb_elements, ext_word_list=set(ext_word_list) - {key})

        return key, value

    def requirements(self, ext_word_list=None, nb_elements=10, variable_nb_elements=True):
        """Looks like this:

        generic_requirements = {
            'public works': [
                'engineering',
                'logistics'
            ],
        }
        """
        if ext_word_list is None:
            ext_word_list = generic_technology.keys()

        if variable_nb_elements:
            nb_elements = self.randomize_nb_elements(nb_elements, min=1)

        return dict(f() for f in repeat(self.generator.requirement, nb_elements))


fake.add_provider(Provider)
