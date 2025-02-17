from django.urls import include, path
from rest_framework.routers import DefaultRouter

from backend.zettle import views

app_name = "zettle"


router = DefaultRouter()
router.register(r"cards", views.ZettleCardViewSet)

urlpatterns = [
    path("api/", include(router.urls)),
    path("cards/", views.ZettleCardView.as_view(), name="zettlecards"),
]
