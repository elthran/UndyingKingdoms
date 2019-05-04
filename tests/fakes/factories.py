import factory
from factory.alchemy import SQLAlchemyModelFactory

from undyingkingdoms import User
from undyingkingdoms.controler.initialize import pick_kingdom
from undyingkingdoms.models import County, Technology


from tests.fakes.mixins import SQLAlcMeta
from tests.fakes.providers import Provider

factory.Faker.add_provider(Provider)


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


class TechFactory(SQLAlchemyModelFactory):
    """Technology factory."""
    class Meta(SQLAlcMeta):
        model = Technology

    name = factory.Faker('tech')
    cost = factory.Faker('pyint', min=250, max=100, step=50)
    max_level = 1
    description = ""
