from uuid import uuid4

from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import UserManager as BaseUserManager
from django.db import models


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    uuid = models.UUIDField(default=uuid4, db_index=True, editable=False)

    class Meta:
        abstract = True
        ordering = ["-created_at"]
        get_latest_by = "created_at"

    def __str__(self):
        return f"{self.__class__.__name__}({self.uuid})"


class UserManager(BaseUserManager):
    pass


class User(BaseModel, AbstractUser):
    objects = UserManager()


class Garden(BaseModel):
    parent = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="children",
    )

    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)

    def __str__(self):
        return self.title


class Location(BaseModel):
    garden = models.ForeignKey(
        "Garden",
        related_name="locations",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)

    def __str__(self):
        return self.title


class CardPlacement(models.Model):
    location = models.ForeignKey("Location", related_name="placements", on_delete=models.CASCADE)
    card = models.ForeignKey("Card", related_name="placements", on_delete=models.CASCADE)
    x = models.IntegerField(default=0)
    y = models.IntegerField(default=0)
    z = models.IntegerField(default=0)


class Tag(BaseModel):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)


class Card(BaseModel):
    title = models.CharField(max_length=255)
    text = models.TextField(blank=True)
    image = models.ImageField(upload_to="cards", blank=True)
    tags = models.ManyToManyField("Tag", related_name="cards")

    def __str__(self):
        return self.title


class Comment(BaseModel):
    card = models.ForeignKey(
        "Card",
        related_name="comments",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    author = models.ForeignKey(
        "User",
        related_name="comments",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    parent = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="children",
    )

    text = models.TextField()
