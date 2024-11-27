from django.core.exceptions import ValidationError
from django.db import models
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
        return f"Cat: {self.name}. Breed: {breed}"

    def clean(self):
        validate_breed_name(self.breed, ValidationError)

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)


