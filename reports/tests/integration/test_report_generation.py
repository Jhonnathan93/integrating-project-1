from datetime import datetime

from django.contrib.auth.models import User
from django.test import TestCase, tag
from django.urls import reverse
from django.utils import timezone

from book.models import History


@tag("integration")
class ReportGenerationIntegrationTests(TestCase):
    def setUp(self) -> None:
        self.staff_user = User.objects.create_user(
            username="staff", password="secure-password", is_staff=True
        )
        self.client.force_login(self.staff_user)

    def test_date_filtered_report_uses_persisted_history_data(self) -> None:
        History.objects.create(
            user=self.staff_user,
            books="Dune",
            topics="Science fiction, Adventure",
            genres="Novel",
            date=timezone.make_aware(datetime(2026, 1, 15, 12, 0)),
        )
        History.objects.create(
            user=self.staff_user,
            books="Old book",
            topics="History",
            genres="Biography",
            date=timezone.make_aware(datetime(2025, 1, 15, 12, 0)),
        )

        response = self.client.get(
            reverse("reports:report"),
            {"fecha_inicio": "2026-01-01", "fecha_fin": "2026-01-31"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["report_available"])
        self.assertEqual(
            response.context["chart_data"]["categories"],
            {"labels": ["Adventure", "Science fiction"], "values": [1, 1]},
        )
        self.assertEqual(
            response.context["chart_data"]["genres"],
            {"labels": ["Novel"], "values": [1]},
        )
