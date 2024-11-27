from rest_framework import viewsets

from spycats.models import SpyCat, Mission
from spycats.serializers import CatListSerializer, CatRetrieveSerializer, CatSerializer


class SpyCatViewSet(viewsets.ModelViewSet):
    model = SpyCat
    queryset = SpyCat.objects.all()

    def get_serializer_class(self):
        if self.action == "list":
            return CatListSerializer
        if self.action == "retrieve":
            return CatRetrieveSerializer

        return CatSerializer

    def get_queryset(self):
        queryset = super().get_queryset()

        if self.action in ["list", "retrieve"]:
            return queryset.prefetch_related("missions")

        return queryset


class MissionViewSet(viewsets.ModelViewSet):
    model = Mission
    queryset = Mission.objects.all()
