from django.db.utils import IntegrityError
from django.test import TestCase
from spycats.models import SpyCat, Mission, Target
from django.core.exceptions import ValidationError


class SpyCatModelTests(TestCase):
    def test_create_valid_spycat(self):
        cat = SpyCat.objects.create(
            name="Agent test",
            breed="Siamese",
            years_of_experience=5,
            salary=1230.00
        )
        self.assertEqual(cat.name, "Agent test")
        self.assertEqual(cat.salary, 1230.00)

    def test_invalid_salary(self):
        with self.assertRaises(ValidationError):
            SpyCat.objects.create(
                name="Agent test 2",
                breed="Persian",
                years_of_experience=23,
                salary=-533.00
            )

    def test_validate_breed_name(self):
        with self.assertRaises(ValidationError):
            cat = SpyCat(
                name="Agent i",
                breed="Invbgf3",
                years_of_experience=3,
                salary=2000.00
            )
            cat.full_clean()  # Trigger validation

    def test_salary_constraint(self):
        cat = SpyCat(
            name="Test name 3",
            breed="Siamese",
            years_of_experience=3,
            salary=0.00
        )
        with self.assertRaises(ValidationError):
            cat.save()


class MissionModelTests(TestCase):
    def setUp(self):
        self.cat = SpyCat.objects.create(
            name="Agent mrmr",
            breed="Siamese",
            years_of_experience=7,
            salary=1500.00
        )

    def test_create_mission_without_cat(self):
        mission = Mission.objects.create(is_complete=False)
        self.assertIsNone(mission.cat)

    def test_assign_cat_to_mission(self):
        mission = Mission.objects.create(is_complete=False, cat=self.cat)
        self.assertEqual(mission.cat, self.cat)

    def test_mission_str(self):
        mission = Mission.objects.create(is_complete=True, cat=self.cat)
        self.assertEqual(str(mission), f"Mission assigned to {self.cat.name}. Status: True")

    def test_open_mission_str(self):
        mission = Mission.objects.create(is_complete=False)
        self.assertEqual(str(mission), f"Open mission with id {mission.id}")


class TargetModelTests(TestCase):
    def setUp(self):
        self.cat = SpyCat.objects.create(
            name="Agent Purr",
            breed="Siamese",
            years_of_experience=10,
            salary=2000.00
        )
        self.mission = Mission.objects.create(is_complete=False, cat=self.cat)

    def test_create_target(self):
        target = Target.objects.create(
            mission=self.mission,
            name="Target test",
            country="Test country",
            notes="Some notes",
            is_complete=False
        )
        self.assertEqual(target.mission, self.mission)
        self.assertEqual(target.name, "Target test")

    def test_target_str(self):
        target = Target.objects.create(
            mission=self.mission,
            name="Target Bravo",
            country="Test country",
            notes="Confidential",
            is_complete=True
        )
        self.assertEqual(str(target), f"Target: {target.name}. Is_complete: {target.is_complete}")

    def test_delete_mission_cascades_targets(self):
        target = Target.objects.create(
            mission=self.mission,
            name="Target Charlie",
            country="test_country",
            notes="note test",
            is_complete=False
        )
        self.mission.delete()
        with self.assertRaises(Target.DoesNotExist):
            Target.objects.get(id=target.id)
