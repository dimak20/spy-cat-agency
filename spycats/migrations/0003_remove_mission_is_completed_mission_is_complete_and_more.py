# Generated by Django 5.1.3 on 2024-11-27 11:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("spycats", "0002_mission_spycat_salary_greater_than_zero_mission_cat"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="mission",
            name="is_completed",
        ),
        migrations.AddField(
            model_name="mission",
            name="is_complete",
            field=models.BooleanField(default=False, verbose_name="is complete"),
        ),
        migrations.AlterField(
            model_name="mission",
            name="cat",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="missions",
                to="spycats.spycat",
            ),
        ),
        migrations.CreateModel(
            name="Target",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100, verbose_name="name")),
                ("country", models.CharField(max_length=100, verbose_name="country")),
                ("notes", models.TextField(blank=True, null=True)),
                (
                    "is_complete",
                    models.BooleanField(default=False, verbose_name="is complete"),
                ),
                (
                    "mission",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="targets",
                        to="spycats.mission",
                    ),
                ),
            ],
        ),
    ]
