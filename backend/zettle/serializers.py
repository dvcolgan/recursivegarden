from rest_framework import serializers

from backend.zettle.models import ZettleCard


class ZettleCardSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(
        read_only=True, default=serializers.CurrentUserDefault()
    )
    tags = serializers.PrimaryKeyRelatedField(
        many=True, queryset=ZettleCard.objects.all(), required=False
    )

    class Meta:
        model = ZettleCard
        fields = [
            "uuid",
            "card_type",
            "author",
            "title",
            "votes",
            "text",
            "image",
            "document",
            "url",
            "content_type",
            "object_id",
            "parent",
            "next",
            "reply_to",
            "tags",
            "slug",
            "x",
            "y",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["uuid", "votes", "created_at", "updated_at"]
