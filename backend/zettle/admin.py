from django.contrib import admin
from django.db.models import Count

from backend.zettle.models import ZettleCard


@admin.register(ZettleCard)
class ZettleCardAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "card_type",
        "author",
        "votes",
        "child_count",
        "created_at",
        "updated_at",
    ]
    list_filter = ["card_type", "author", "created_at", "updated_at"]
    search_fields = ["title", "text", "url", "author__username"]
    readonly_fields = ["created_at", "updated_at", "uuid"]
    raw_id_fields = ["parent", "next", "reply_to"]
    filter_horizontal = ["tags"]

    fieldsets = [
        (None, {"fields": ["card_type", "author", "title", "votes"]}),
        (
            "Content",
            {
                "fields": ["text", "image", "document", "url"],
            },
        ),
        (
            "Generic Foreign Key",
            {
                "fields": ["content_type", "object_id"],
            },
        ),
        (
            "Relationships",
            {
                "fields": ["parent", "next", "reply_to", "tags"],
            },
        ),
        (
            "Location",
            {
                "fields": ["slug", "x", "y"],
            },
        ),
        (
            "Metadata",
            {
                "fields": ["uuid", "created_at", "updated_at"],
            },
        ),
    ]

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(child_count=Count("children"))

    def child_count(self, obj):
        return obj.child_count

    child_count.admin_order_field = "child_count"
    child_count.short_description = "Children"

    def save_model(self, request, obj, form, change):
        if not obj.author:
            obj.author = request.user
        super().save_model(request, obj, form, change)
