from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from spycats.models import SpyCat, Mission, Target



class MissionViewSetTests(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.cat = SpyCat.objects.create(
            name="Agent Whiskers",
            years_of_experience=5,
            breed="Siamese",
            salary=1000
        )

        self.mission = Mission.objects.create(
            is_complete=False
        )

        self.targets = [
            Target.objects.create(
                mission=self.mission,
                name=f"Target {i}",
                country="Testland",
                notes="Confidential",
                is_complete=False
            )
            for i in range(3)
        ]

    def test_assign_cat_to_mission(self):
        response = self.client.patch(
            reverse("spycats:mission-assign-cat", kwargs={"pk": self.mission.id}),
            data={"cat": self.cat.id},
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.mission.refresh_from_db()
        self.assertEqual(self.mission.cat, self.cat)

    def test_assign_cat_to_completed_mission(self):
        self.mission.is_complete = True
        self.mission.save()

        response = self.client.patch(
            reverse("spycats:mission-assign-cat", kwargs={"pk": self.mission.id}),
            data={"cat": self.cat.id},
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Cannot assign a cat to a completed mission.", response.data["detail"])


    def test_update_target_notes(self):
        target = self.targets[0]
        response = self.client.patch(
            reverse("spycats:mission-detail", kwargs={"pk": self.mission.id}),
            data={
                "targets": [
                    {"id": target.id, "notes": "Updated notes"}
                ]
            },
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        target.refresh_from_db()
        self.assertEqual(target.notes, "Updated notes")

    def test_update_completed_target(self):
        target = self.targets[0]
        target.is_complete = True
        target.save()

        response = self.client.patch(
            reverse("spycats:mission-detail", kwargs={"pk": self.mission.id}),
            data={
                "targets": [
                    {"id": target.id, "notes": "New notes"}
                ]
            },
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Cannot update fields of a completed target", response.data["non_field_errors"])

    def test_complete_all_targets_and_mission(self):
        response = self.client.patch(
            reverse("spycats:mission-detail", kwargs={"pk": self.mission.id}),
            data={
                "targets": [
                    {"id": target.id, "is_complete": True}
                    for target in self.targets
                ]
            },
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.mission.refresh_from_db()
        self.assertTrue(self.mission.is_complete)
