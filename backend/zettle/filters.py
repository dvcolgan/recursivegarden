from django_filters import CharFilter
from django_filters.rest_framework import FilterSet

from backend.zettle.models import ZettleCard


class ZettleCardFilter(FilterSet):
    title = CharFilter(lookup_expr="icontains")
    tag = CharFilter(field_name="tags__title", lookup_expr="icontains")
    text = CharFilter(lookup_expr="icontains")

    class Meta:
        model = ZettleCard
        fields = {
            "card_type": ["exact"],
            "author": ["exact"],
            "created_at": ["gte", "lte"],
            "x": ["exact", "gte", "lte"],
            "y": ["exact", "gte", "lte"],
        }
