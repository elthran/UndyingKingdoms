from factory import LazyAttribute, Factory, Faker
from faker.providers import BaseProvider

from tests import bp
from undyingkingdoms.controler.initialize import pick_kingdom
from undyingkingdoms.models import User, County


# county_names = ['daspeoland', 'ieswouya', 'iofrary', 'zufra', 'straodan', 'spueque', 'otral', 'awhos', 'floey bril', 'glaex smea']
#
#
# class Provider(BaseProvider):
#     def county_name(self):
#         return str(Faker('word', ext_word_list=county_names)).title()
#
#
# Faker.add_provider(Provider)
#
# leader_names = ['']


class UserFactory(Factory):
    class Meta:
        model = User

    username = Faker('user_name')
    email = Faker('email')
    password = 'password'


# class CountyFactory(Factory):
#     class Meta:
#         model = County
#
#     user = UserFactory()
#     kingdom_id = LazyAttribute(lambda a: pick_kingdom(a.user, False).id)
#     county_name = Faker('county_name')
#     leader_name = Faker('name', ext_word_list=leader_names)
#     user_id = LazyAttribute(lambda a: a.user.id)
    # race
    # title
    # background
