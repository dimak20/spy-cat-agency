from django.urls import path, include
from rest_framework.routers import DefaultRouter

from spycats.views import SpyCatViewSet, MissionViewSet

app_name = "spycats"

router = DefaultRouter()
router.register("cats", SpyCatViewSet)
router.register("missions", MissionViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
