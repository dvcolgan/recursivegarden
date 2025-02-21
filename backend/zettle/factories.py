import factory
from factory.django import DjangoModelFactory

from backend.users.factories import UserFactory
from backend.zettle.models import ZettleCard


class ZettleCardFactory(DjangoModelFactory):
    class Meta:
        model = ZettleCard

    title = factory.Sequence(lambda n: f"Test Card {n}")
    card_type = ZettleCard.CardType.TEXT
    text = factory.Faker("paragraph")
    author = factory.SubFactory(UserFactory)
    votes = 1
