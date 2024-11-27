from django.db import transaction
from rest_framework import serializers

from spycats.models import SpyCat, Mission, Target
from spycats.validators import validate_breed_name


class TargetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Target
        fields = ["id", "name", "country", "notes", "is_complete"]


class TargetUpdateSerializer(serializers.Serializer):
    id = serializers.CharField()
    is_complete = serializers.BooleanField(required=False)
    notes = serializers.CharField(required=False)


class MissionSerializer(serializers.ModelSerializer):
    targets = TargetSerializer(many=True, read_only=False, allow_empty=False)
    is_complete = serializers.BooleanField(read_only=True)
    cat = serializers.CharField(read_only=True)

    class Meta:
        model = Mission
        fields = ["id", "cat", "is_complete", "targets"]

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
    targets = serializers.SlugRelatedField(read_only=True, slug_field="id", many=True)


class MissionAssignCatSerializer(serializers.ModelSerializer):
    cat = serializers.PrimaryKeyRelatedField(queryset=SpyCat.objects.all())

    class Meta:
        model = Mission
        fields = ["cat"]


class MissionUpdateSerializer(serializers.ModelSerializer):
    targets = TargetUpdateSerializer(many=True, read_only=False, allow_empty=False)

    class Meta:
        model = Mission
        fields = ["targets"]

    def validate(self, data):

        if self.instance.is_complete:
            raise serializers.ValidationError(
                "Cannot update a completed mission."
            )

        for target_data in data.get("targets", []):
            try:
                target = Target.objects.get(id=target_data["id"])
            except Target.DoesNotExist:
                raise serializers.ValidationError(
                    f"Target with ID {target_data['id']} does not exist."
                )

            if target.is_complete and not target_data.get("is_complete", False):
                raise serializers.ValidationError(
                    "Cannot update fields of a completed target"
                )

        return data

    def update(self, instance: Mission, validated_data):
        targets = validated_data.get("targets", [])
        mission = instance

        with transaction.atomic():
            for target_data in targets:
                target_id = target_data.get("id")
                if not target_id:
                    raise serializers.ValidationError("Target ID is required")

                try:
                    target_to_update = Target.objects.get(id=target_id)
                except Target.DoesNotExist:
                    raise serializers.ValidationError(f"Target with ID {target_id} does not exist")

                if target_to_update.mission != mission:
                    raise serializers.ValidationError(f"Target with ID {target_id} is assigned to another mission")

                for key, value in target_data.items():
                    if hasattr(target_to_update, key) and value is not None:
                        setattr(target_to_update, key, value)

                target_to_update.save()

            if all(target.is_complete for target in mission.targets.all()):
                mission.is_complete = True
                mission.save()

        return instance


class CatSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpyCat
        fields = ["id", "name", "years_of_experience", "breed", "salary"]


class CatCreateSerializer(serializers.ModelSerializer):
    """
    A separate serializer is needed because
    you don’t have to validate the breed every time
    and don’t access a third-party API
    """

    class Meta:
        model = SpyCat
        fields = ["id", "name", "years_of_experience", "breed", "salary"]

    def validate_salary(self, value):
        if value <= 0:
            raise serializers.ValidationError("Salary must be a positive number")

    def validate_breed(self, value):
        print(f"Validating breed: {value}")
        validate_breed_name(value, serializers.ValidationError)


class CatListSerializer(serializers.ModelSerializer):
    missions = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = SpyCat
        fields = ["id", "name", "years_of_experience", "breed", "salary", "missions"]


class CatRetrieveSerializer(CatListSerializer):
    missions = MissionSerializer(many=True, read_only=True)
