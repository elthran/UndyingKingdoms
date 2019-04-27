import factory
from factory.alchemy import SQLAlchemyModelFactory
from faker.providers import BaseProvider
import faker

from extensions import flask_db
from tests import bp
from undyingkingdoms.controler.initialize import pick_kingdom
from undyingkingdoms.models import User, County
from undyingkingdoms.static.metadata.metadata import metadata_races, metadata_backgrounds, metadata_titles

county_names = ['Daspeoland', 'Ieswouya', 'Iofrary', 'Zufra', 'Straodan', 'Spueque', 'Otral', 'Awhos', 'Floey Bril', 'Glaex Smea']

leader_names = ['Smartsprinter', 'Mossfollower', 'Mildstone', 'Fourtree', 'Wheattide', 'Netherguard', 'Terrastriker', 'Freegloom', 'Talltail', 'Heartmark']


fake = faker.Faker()


class Provider(BaseProvider):
    def county(self):
        return fake.word(ext_word_list=county_names)

    def leader(self):
        return fake.word(ext_word_list=leader_names)

    def race(self):
        return fake.word(ext_word_list=metadata_races)

    def title(self):
        return fake.word(ext_word_list=metadata_titles)

    def background(self):
        return fake.word(ext_word_list=metadata_backgrounds)


factory.Faker.add_provider(Provider)


class SQLAlcMeta:
    sqlalchemy_session = flask_db.session
    sqlalchemy_session_persistence = 'commit'


class UserFactory(SQLAlchemyModelFactory):
    class Meta(SQLAlcMeta):
        model = User

    username = factory.Faker('user_name')
    email = factory.LazyAttribute(lambda a: a.username + "@email.ca")
    password = 'password'


class CountyFactory(SQLAlchemyModelFactory):
    class Meta(SQLAlcMeta):
        model = County

    user = UserFactory.build()
    kingdom_id = factory.LazyAttribute(lambda a: pick_kingdom(a.user, False).id)
    name = factory.Faker('county')
    leader = factory.Faker('leader')
    race = factory.Faker('race')
    title = factory.Faker('title')
    background = factory.Faker('background')
