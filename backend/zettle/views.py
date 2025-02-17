from django.views.generic import TemplateView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser

from backend.zettle.filters import ZettleCardFilter
from backend.zettle.models import ZettleCard
from backend.zettle.serializers import ZettleCardSerializer


class ZettleCardViewSet(viewsets.ModelViewSet):
    queryset = ZettleCard.objects.all()
    serializer_class = ZettleCardSerializer
    parser_classes = (MultiPartParser, FormParser, JSONParser)
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_class = ZettleCardFilter
    search_fields = ["title", "text", "tags__title"]
    ordering_fields = ["created_at", "updated_at", "votes", "title"]
    ordering = ["-created_at"]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class ZettleCardView(TemplateView):
    template_name = "zettle/zettlecards.html"
