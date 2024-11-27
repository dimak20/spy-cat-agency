from django.core.exceptions import ObjectDoesNotExist
from rest_framework import viewsets, status, mixins
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from spycats.models import SpyCat, Mission
from spycats.serializers import CatListSerializer, CatRetrieveSerializer, CatSerializer, MissionSerializer, \
    MissionListSerializer, MissionAssignCatSerializer


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


class MissionViewSet(
    GenericViewSet,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
):
    model = Mission
    queryset = Mission.objects.all()

    def get_serializer_class(self):
        if self.action == "list":
            return MissionListSerializer
        if self.action == "assign-cat":
            return MissionAssignCatSerializer
        return MissionSerializer

    def destroy(self, request, *args, **kwargs):

        mission = self.get_object()

        if mission.cat is not None:
            return Response(
                {"detail": "Cannot delete mission when assigned to a cat"},
                status=status.HTTP_400_BAD_REQUEST
            )

        self.perform_destroy(mission)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=["PATCH", "PUT"], detail=True, url_path="assign-cat")
    def assign_cat(self, request, pk: int | None =None) -> Response:

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
