from django.db import connection
from django.test import TestCase, tag


@tag("integration")
class DatabaseConnectionIntegrationTests(TestCase):
    def test_default_database_accepts_queries(self) -> None:
        """Verify that Django can use the isolated test database connection."""

        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            result = cursor.fetchone()

        self.assertEqual(result, (1,))
