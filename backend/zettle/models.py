from pathlib import Path

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

from backend.core.models import BaseModel


def format_filename_as_title(filename: str) -> str:
    name = Path(filename).stem
    name = name.replace("-", " ").replace("_", " ")
    return name.capitalize()


def get_image_upload_path(instance, filename):
    if not instance.title:
        instance.title = format_filename_as_title(filename)
    ext = Path(filename).suffix
    return f"images/{instance.uuid}{ext}"


def get_file_upload_path(instance, filename):
    if not instance.title:
        instance.title = format_filename_as_title(filename)
    ext = Path(filename).suffix
    return f"files/{instance.uuid}{ext}"


class ZettleCard(BaseModel):
    class CardType(models.TextChoices):
        TEXT = "text", "Text Card"
        IMAGE = "image", "Image Card"
        URL = "url", "URL Card"
        MODEL = "model", "Model Reference Card"
        TOPIC = "topic", "Topic Card"

    # Metadata
    card_type = models.CharField(
        max_length=20, choices=CardType.choices, default=CardType.TEXT
    )
    author = models.ForeignKey(
        "users.User",
        related_name="cards",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    title = models.CharField(max_length=1023, blank=True)
    votes = models.IntegerField(default=1)

    # Content of various types
    text = models.TextField(blank=True)
    image = models.ImageField(
        max_length=1023,
        null=True,
        blank=True,
        upload_to=get_image_upload_path,
    )
    document = models.FileField(
        max_length=1023, upload_to=get_file_upload_path, null=True, blank=True
    )
    url = models.URLField(max_length=1023, blank=True)
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = GenericForeignKey("content_type", "object_id")

    # Relationships
    parent = models.ForeignKey(
        "self",
        related_name="children",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    next = models.OneToOneField(
        "self",
        related_name="prev",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    reply_to = models.ForeignKey(
        "self",
        related_name="replies",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    # Location
    tags = models.ManyToManyField("self", blank=True)
    slug = models.SlugField(max_length=255, blank=True)
    x = models.IntegerField(null=True, blank=True)
    y = models.IntegerField(null=True, blank=True)

    @property
    def template_name(self):
        """Get the appropriate template for this card type."""
        return f"zettle/card_types/{self.card_type}.html"

    class Meta:
        indexes = [
            models.Index(fields=["card_type"]),
            models.Index(fields=["slug"]),
            models.Index(fields=["content_type", "object_id"]),
        ]

        verbose_name = "Zettle Card"
        verbose_name_plural = "Zettle Cards"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.title or 'Untitled'} ({self.get_card_type_display()})"
