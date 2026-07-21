from django.db import connection
from django.test import TestCase, tag
from django.urls import reverse


@tag("integration")
class DatabaseConnectionIntegrationTests(TestCase):
    def test_default_database_accepts_queries(self) -> None:
        """Verify that Django can use the isolated test database connection."""

        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            result = cursor.fetchone()

        self.assertEqual(result, (1,))

    def test_health_endpoint_reports_database_readiness(self) -> None:
        response = self.client.get(reverse("health:health"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "ok"})
