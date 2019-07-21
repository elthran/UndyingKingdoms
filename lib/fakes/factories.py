import factory
from factory.alchemy import SQLAlchemyModelFactory

import app.models.exports as models
from app.controler.initialize import pick_kingdom
from lib.fakes.mixins import SQLAlcMeta
from lib.fakes.providers import Provider

factory.Faker.add_provider(Provider)


class UserFactory(SQLAlchemyModelFactory):
    class Meta(SQLAlcMeta):
        model = models.User

    username = factory.Faker('user_name')
    email = factory.LazyAttribute(lambda a: a.username + "@email.ca")
    password = 'password'


class CountyFactory(SQLAlchemyModelFactory):
    class Meta(SQLAlcMeta):
        model = models.County

    user = UserFactory.build()
    kingdom_id = factory.LazyAttribute(lambda a: pick_kingdom(a.user, False).id)
    name = factory.Faker('county')
    leader = factory.Faker('leader')
    race = factory.Faker('race')
    title = factory.Faker('title')
    background = factory.Faker('background')


class TechFactory(SQLAlchemyModelFactory):
    """Technology factory."""
    class Meta(SQLAlcMeta):
        model = models.Technology

    name = factory.Faker('tech')
    cost = factory.Faker('pyint', min=250, max=100, step=50)
    max_level = 1
    description = ""
