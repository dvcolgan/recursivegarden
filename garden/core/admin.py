from django.contrib import admin

from garden.core.models import Card, CardPlacement, Comment, Garden, Location, Tag, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "created_at", "is_staff")
    search_fields = ("username", "email")
    list_filter = ("is_staff", "is_active", "created_at")
    date_hierarchy = "created_at"


@admin.register(Garden)
class GardenAdmin(admin.ModelAdmin):
    list_display = ("title", "slug", "parent", "created_at")
    search_fields = ("title", "slug")
    list_filter = ("created_at",)
    prepopulated_fields = {"slug": ("title",)}
    date_hierarchy = "created_at"


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ("title", "slug", "garden", "created_at")
    search_fields = ("title", "slug", "garden__title")
    list_filter = ("garden", "created_at")
    prepopulated_fields = {"slug": ("title",)}
    date_hierarchy = "created_at"


@admin.register(CardPlacement)
class CardPlacementAdmin(admin.ModelAdmin):
    list_display = ("card", "location", "x", "y", "z")
    search_fields = ("card__title", "location__title")
    list_filter = ("location",)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("title", "slug", "created_at")
    search_fields = ("title", "slug")
    prepopulated_fields = {"slug": ("title",)}
    date_hierarchy = "created_at"


@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = ("title", "created_at")
    search_fields = ("title", "text")
    filter_horizontal = ("tags",)
    date_hierarchy = "created_at"
    list_filter = ("tags", "created_at")


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("card", "author", "parent", "created_at")
    search_fields = ("text", "author__username", "card__title")
    list_filter = ("created_at", "author")
    date_hierarchy = "created_at"
    raw_id_fields = ("author", "parent")
