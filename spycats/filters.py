import django_filters

from spycats.models import SpyCat


class SpyCatFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(
        field_name="name",
        lookup_expr="icontains"
    )
    breed = django_filters.CharFilter(
        field_name="breed",
        lookup_expr="icontains"
    )
    salary_more_than = django_filters.NumberFilter(
        field_name="salary",
        lookup_expr="gte"
    )
    salary_less_than = django_filters.NumberFilter(
        field_name="salary",
        lookup_expr="lte"
    )

    class Meta:
        model = SpyCat
        fields = [
            "name",
            "breed",
            "salary",
            "years_of_experience"

        ]


class MissionFilter(django_filters.FilterSet):
    is_complete = django_filters.BooleanFilter(
        field_name="is_complete",
        lookup_expr="exact"
    )
