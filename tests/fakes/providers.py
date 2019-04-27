import faker
from faker.providers import BaseProvider

from undyingkingdoms.blueprints.admin.metadata import bot_county_prefix, bot_county_suffix, bot_leader_prefix, \
    bot_leader_suffix
from undyingkingdoms.static.metadata.metadata import metadata_races, metadata_titles, metadata_backgrounds
from undyingkingdoms.static.metadata.metadata_research_all import generic_technology, generic_requirements

fake = faker.Faker()


# noinspection PyMethodMayBeStatic
class Provider(BaseProvider):
    def county(self):
        return fake.word(ext_word_list=bot_county_prefix) + fake.word(ext_word_list=bot_county_suffix)

    def leader(self):
        return fake.word(ext_word_list=bot_leader_prefix) + fake.word(ext_word_list=bot_leader_suffix)

    def race(self):
        return fake.word(ext_word_list=metadata_races)

    def title(self):
        return fake.word(ext_word_list=metadata_titles)

    def background(self):
        return fake.word(ext_word_list=metadata_backgrounds)

    def tech(self):
        return fake.word(ext_word_list=generic_technology)

    def requirements(self):
        """Return a randomly size/shaped dict of requirements.


        """
        return fake.word(ext_word_list=generic_requirements)
