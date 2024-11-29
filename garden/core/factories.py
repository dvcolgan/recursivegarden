import factory
from django.utils.text import slugify
from factory.django import DjangoModelFactory

from garden.core import models


class UserFactory(DjangoModelFactory):
    class Meta:
        model = models.User

    username = factory.Sequence(lambda n: f"user_{n}")
    email = factory.LazyAttribute(lambda obj: f"{obj.username}@example.com")
    password = factory.PostGenerationMethodCall("set_password", "password123")


class GardenFactory(DjangoModelFactory):
    class Meta:
        model = models.Garden

    title = factory.Sequence(lambda n: f"Garden {n}")
    slug = factory.LazyAttribute(lambda obj: slugify(obj.title))
    parent = None


class LocationFactory(DjangoModelFactory):
    class Meta:
        model = models.Location

    garden = factory.SubFactory(GardenFactory)
    title = factory.Sequence(lambda n: f"Location {n}")
    slug = factory.LazyAttribute(lambda obj: slugify(obj.title))


class TagFactory(DjangoModelFactory):
    class Meta:
        model = models.Tag

    title = factory.Sequence(lambda n: f"Tag {n}")
    slug = factory.LazyAttribute(lambda obj: slugify(obj.title))


class CardFactory(DjangoModelFactory):
    class Meta:
        model = models.Card

    title = factory.Sequence(lambda n: f"Card {n}")
    text = factory.Faker("paragraph")
    image = factory.django.ImageField(color="blue")

    @factory.post_generation
    def tags(self, create, extracted, **kwargs):
        if not create or not extracted:
            return

        for tag in extracted:
            self.tags.add(tag)


class CardPlacementFactory(DjangoModelFactory):
    class Meta:
        model = models.CardPlacement

    location = factory.SubFactory(LocationFactory)
    card = factory.SubFactory(CardFactory)
    x = factory.Faker("random_int", min=0, max=1000)
    y = factory.Faker("random_int", min=0, max=1000)
    z = factory.Faker("random_int", min=0, max=10)


class CommentFactory(DjangoModelFactory):
    class Meta:
        model = models.Comment

    card = factory.SubFactory(CardFactory)
    author = factory.SubFactory(UserFactory)
    parent = None
    text = factory.Faker("paragraph")
