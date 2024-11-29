from django.core.management.base import BaseCommand
from django.db import transaction

from garden.core.factories import GardenFactory
from garden.core.models import User


class Command(BaseCommand):
    help = "Fill the database with fixtures for manual testing and demos."

    @transaction.atomic
    def handle(self, *args, **options):
        _admin_user = User.objects.create_superuser("admin", "admin@example.com", "wemusttendourgarden")

        # Gardens
        _dvcolgan = GardenFactory(title="DVColgan", slug="dvcolgan")
        _livestream = GardenFactory(title="Livestream", slug="livestream")
