from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import SET_NULL, Q, CASCADE
from django.utils.translation import gettext as _

from spycats.validators import validate_breed_name


class SpyCat(models.Model):
    name = models.CharField(_("name"), max_length=100)
    breed = models.CharField(_("breed"), max_length=100)
    years_of_experience = models.PositiveIntegerField(
        _("years of experience")
    )
    salary = models.DecimalField(
        _("salary"),
        max_digits=7,
        decimal_places=2
    )

    def __str__(self) -> str:
        return f"Cat: {self.name}. Breed: {self.breed}"

    def clean(self):
        validate_breed_name(self.breed, ValidationError)

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=Q(salary__gt=0),
                name="salary_greater_than_zero"
            ),
        ]


class Mission(models.Model):
    cat = models.ForeignKey(
        SpyCat,
        on_delete=SET_NULL,
        blank=True,
        null=True,
        related_name="missions"
    )
    is_complete = models.BooleanField(
        _("is complete"),
        default=False
    )

    def __str__(self) -> str:
        if self.cat:
            return f"Mission assigned to {self.cat.name}. Status: {self.is_complete}"
        return f"Open mission with id {self.id}"


class Target(models.Model):
    mission = models.ForeignKey(
        Mission,
        on_delete=CASCADE,
        related_name="targets"
    )
    name = models.CharField(
        _("name"),
        max_length=100
    )
    country = models.CharField(
        _("country"),
        max_length=100
    )
    notes = models.TextField(
        blank=True,
        null=True
    )
    is_complete = models.BooleanField(
        _("is complete"),
        default=False
    )

    def __str__(self) -> str:
        return f"Target: {self.name}. Is_complete: {self.is_complete}"
