from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class ReportsViewTests(TestCase):
    def setUp(self) -> None:
        self.staff_user = User.objects.create_user(
            username="staff", password="password", is_staff=True
        )

    def test_reports_requires_staff_user(self) -> None:
        regular_user = User.objects.create_user(username="reader", password="password")
        self.client.force_login(regular_user)

        response = self.client.get(reverse("reports:report"))

        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("accounts:login"), response["Location"])

    def test_reports_generates_unfiltered_chart_data_for_staff_user(self) -> None:
        self.client.force_login(self.staff_user)

        response = self.client.get(reverse("reports:report"))

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["report_available"])
        self.assertIn("chart_data", response.context)
        self.assertEqual(response.context["chart_data"]["categories"]["labels"], [])

    def test_reports_accepts_a_complete_date_range(self) -> None:
        self.client.force_login(self.staff_user)

        response = self.client.get(
            reverse("reports:report"),
            {"fecha_inicio": "2026-01-01", "fecha_fin": "2026-01-31"},
        )

        self.assertTrue(response.context["report_available"])
        self.assertContains(response, "entre 2026-01-01 y 2026-01-31")

    def test_reports_requires_both_filter_dates(self) -> None:
        self.client.force_login(self.staff_user)

        response = self.client.get(
            reverse("reports:report"), {"fecha_inicio": "2026-01-01"}
        )

        self.assertFalse(response.context["report_available"])
        self.assertContains(response, "Indica ambas fechas para filtrar el informe.")
