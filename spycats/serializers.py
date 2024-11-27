from django.db import transaction
from rest_framework import serializers

from spycats.models import SpyCat, Mission, Target
from spycats.validators import validate_breed_name


class TargetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Target
        fields = [
            "id",
            "name",
            "country",
            "notes",
            "is_complete"
        ]


class MissionSerializer(serializers.ModelSerializer):
    targets = TargetSerializer(
        many=True,
        read_only=False,
        allow_empty=False
    )
    is_complete = serializers.BooleanField(read_only=True)
    cat = serializers.CharField(read_only=True)

    class Meta:
        model = Mission
        fields = [
            "id",
            "cat",
            "is_complete",
            "targets"
        ]

    def create(self, validated_data):
        with transaction.atomic():
            targets = validated_data.pop("targets", [])
            mission = Mission.objects.create(**validated_data)

            if len(targets) > 3:
                raise serializers.ValidationError(
                    "Number of targets must be in range from 1 to 3"
                )

            for target in targets:
                Target.objects.create(mission=mission, **target)

        return mission


class MissionListSerializer(MissionSerializer):
    targets = serializers.SlugRelatedField(
        read_only=True,
        slug_field="id",
        many=True
    )


class MissionAssignCatSerializer(serializers.ModelSerializer):
    cat = serializers.PrimaryKeyRelatedField(queryset=SpyCat.objects.all())

    class Meta:
        model = Mission
        fields = ["cat"]


class CatSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpyCat
        fields = [
            "id",
            "name",
            "years_of_experience",
            "breed",
            "salary"
        ]


class CatCreateSerializer(serializers.ModelSerializer):
    """
    A separate serializer is needed because
    you don’t have to validate the breed every time
    and don’t access a third-party API
    """

    class Meta:
        model = SpyCat
        fields = [
            "id",
            "name",
            "years_of_experience",
            "breed",
            "salary"
        ]

    def validate_salary(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                "Salary must be a positive number"
            )

    def validate_breed(self, value):
        print(f"Validating breed: {value}")
        validate_breed_name(value, serializers.ValidationError)


class CatListSerializer(serializers.ModelSerializer):
    missions = serializers.PrimaryKeyRelatedField(
        many=True,
        read_only=True
    )

    class Meta:
        model = SpyCat
        fields = [
            "id",
            "name",
            "years_of_experience",
            "breed",
            "salary",
            "missions"
        ]


class CatRetrieveSerializer(CatListSerializer):
    missions = MissionSerializer(many=True, read_only=True)
