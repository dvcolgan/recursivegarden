from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from django.db import transaction

from backend.users.models import User
from backend.zettle.models import ZettleCard

DEMO_USERS = [
    ("superadmin", "Super Admin User", "admin@example.com"),
    ("sarah", "Sarah Developer", "sarah@example.com"),
    ("mike", "Mike Designer", "mike@example.com"),
    ("alex", "Alex Writer", "alex@example.com"),
]


DEMO_CARDS = [
    # Basic text cards with hierarchy
    {
        "card_type": "topic",
        "title": "Project Management",
        "text": "Main hub for project management concepts and techniques.",
        "author": "sarah",
        "x": 0,
        "y": 0,
        "children": [
            {
                "card_type": "text",
                "title": "Agile Methodology",
                "text": "Agile is an iterative approach to project management...",
                "x": -100,
                "y": 100,
            },
            {
                "card_type": "text",
                "title": "Scrum Framework",
                "text": "Scrum is a lightweight framework that helps people...",
                "x": 100,
                "y": 100,
            },
        ],
    },
    # URL card with replies
    {
        "card_type": "url",
        "title": "Interesting Article on Neural Networks",
        "url": "https://example.com/neural-networks",
        "text": "Great introduction to neural networks",
        "author": "mike",
        "x": 200,
        "y": -100,
        "replies": [
            {
                "card_type": "text",
                "title": "Great Resource",
                "text": "This helped me understand backpropagation!",
                "author": "alex",
            },
            {
                "card_type": "text",
                "title": "Additional Context",
                "text": "Here's a practical example...",
                "author": "sarah",
            },
        ],
    },
    # Image card with tags
    {
        "card_type": "image",
        "title": "System Architecture Diagram",
        "text": "High-level overview of our system architecture",
        "author": "mike",
        "x": -200,
        "y": -200,
        "generate_image": True,  # We'll create a simple image
        "tag_titles": ["Architecture", "Documentation"],
    },
    # Linked sequence of cards
    {
        "card_type": "text",
        "title": "Getting Started",
        "text": "Step 1: Installation",
        "author": "sarah",
        "x": 300,
        "y": 300,
        "sequence": [
            {
                "title": "Configuration",
                "text": "Step 2: Configure your environment",
            },
            {
                "title": "First Steps",
                "text": "Step 3: Create your first project",
            },
        ],
    },
]


class Command(BaseCommand):
    help = "Fill the database with demo data."

    def create_card(self, data, parent=None, author_user=None):
        # Get the author
        author = author_user or User.objects.get(
            username=data.get("author", "superadmin")
        )

        # Remove nested data
        children = data.pop("children", [])
        replies = data.pop("replies", [])
        sequence = data.pop("sequence", [])
        tag_titles = data.pop("tag_titles", [])
        generate_image = data.pop("generate_image", False)

        # Create the card
        card = ZettleCard.objects.create(
            author=author,
            parent=parent,
            **{k: v for k, v in data.items() if k not in ["author"]},
        )

        # Generate demo image if needed
        if generate_image:
            # Create a simple colored square as demo image
            img_content = b"GIF89a\x01\x00\x01\x00\x80\x00\x00\xff\xff\xff\xff\xff\xff!\xf9\x04\x01\x00\x00\x00\x00,\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02D\x01\x00;"
            card.image.save(f"demo_image_{card.uuid}.gif", ContentFile(img_content))

        # Create tag cards and add them
        for tag_title in tag_titles:
            tag_card, _ = ZettleCard.objects.get_or_create(
                card_type=ZettleCard.CardType.TOPIC,
                title=tag_title,
                defaults={"author": author},
            )
            card.tags.add(tag_card)

        # Create child cards
        for child_data in children:
            self.create_card(child_data, parent=card, author_user=author)

        # Create reply cards
        for reply_data in replies:
            reply_data["reply_to"] = card
            self.create_card(reply_data)

        # Create sequence cards
        prev_card = card
        for seq_data in sequence:
            seq_data["card_type"] = ZettleCard.CardType.TEXT
            seq_data["author"] = author
            next_card = self.create_card(seq_data)
            prev_card.next = next_card
            prev_card.save()
            prev_card = next_card

        return card

    @transaction.atomic
    def handle(self, *args, **options):
        # Create users
        for username, full_name, email in DEMO_USERS:
            user = User.objects.create_user(
                username=username, email=email, password="password123"
            )
            first_name, last_name = full_name.split(" ", 1)
            user.first_name = first_name
            user.last_name = last_name
            user.is_staff = username == "superadmin"
            user.is_superuser = username == "superadmin"
            user.save()

            self.stdout.write(self.style.SUCCESS(f"Created user: {username}"))

        # Create demo cards
        self.stdout.write(self.style.SUCCESS("\nCreating demo cards..."))

        for card_data in DEMO_CARDS:
            card = self.create_card(card_data.copy())
            self.stdout.write(self.style.SUCCESS(f"Created card: {card.title}"))

        self.stdout.write(self.style.SUCCESS("Successfully created demo data"))

        self.stdout.write(
            self.style.SUCCESS(
                "\nDemo credentials:\nUsername: superadmin\nPassword: password123\n"
            )
        )
