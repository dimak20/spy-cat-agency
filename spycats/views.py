from django.core.exceptions import ObjectDoesNotExist
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from spycats.filters import SpyCatFilter, MissionFilter
from spycats.models import SpyCat, Mission
from spycats.schemas import cat_filter_parameters, mission_filter_parameters
from spycats.serializers import (
    CatListSerializer,
    CatRetrieveSerializer,
    CatSerializer,
    MissionSerializer,
    MissionListSerializer,
    MissionAssignCatSerializer,
    MissionUpdateSerializer
)


class SpyCatViewSet(viewsets.ModelViewSet):
    model = SpyCat
    queryset = SpyCat.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = SpyCatFilter

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

    @extend_schema(parameters=cat_filter_parameters)
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class MissionViewSet(viewsets.ModelViewSet):
    model = Mission
    queryset = Mission.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = MissionFilter

    def get_serializer_class(self):
        if self.action == "list":
            return MissionListSerializer
        if self.action == "assign-cat":
            return MissionAssignCatSerializer
        if self.action in ["update", "partial_update"]:
            return MissionUpdateSerializer
        return MissionSerializer

    def get_queryset(self):
        queryset = super().get_queryset()

        if self.action in ["list", "retrieve"]:
            return queryset.select_related().prefetch_related("targets")

        return queryset

    def destroy(self, request, *args, **kwargs):

        mission = self.get_object()

        if mission.cat is not None:
            return Response(
                {"detail": "Cannot delete mission when assigned to a cat"},
                status=status.HTTP_400_BAD_REQUEST
            )

        self.perform_destroy(mission)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @extend_schema(parameters=mission_filter_parameters)
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @action(
        methods=["PATCH", "PUT"],
        detail=True,
        url_path="assign-cat"
    )
    def assign_cat(self, request, pk: int | None = None) -> Response:

        mission = self.get_object()

        if mission.is_complete:
            return Response(
                {"detail": "Cannot assign a cat to a completed mission."},
                status=status.HTTP_400_BAD_REQUEST
            )

        cat_id = request.data.get("cat")

        if not cat_id:
            return Response(
                {"detail": "Cat ID is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            cat = SpyCat.objects.get(id=cat_id)
        except ObjectDoesNotExist:
            return Response(
                {"detail": "Cat with the given ID does not exist."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if cat.missions.filter(is_complete=False).exists():
            return Response(
                {"detail": "The cat is already assigned to another mission."},
                status=status.HTTP_400_BAD_REQUEST
            )

        mission.cat = cat
        mission.save()

        return Response(
            {"detail": "Cat assigned successfully."},
            status=status.HTTP_200_OK
        )
