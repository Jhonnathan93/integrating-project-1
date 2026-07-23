import importlib
import os
from unittest.mock import patch

from django.test import SimpleTestCase


class DatabaseSettingsTests(SimpleTestCase):
    def setUp(self):
        self.settings_module = importlib.import_module("BookNexus.settings")

    def tearDown(self):
        importlib.reload(self.settings_module)

    def _reload_settings(self, database_url):
        with patch.dict(os.environ, {"DATABASE_URL": database_url}, clear=False):
            return importlib.reload(self.settings_module)

    def test_uses_sqlite_when_database_url_is_empty(self):
        project_settings = self._reload_settings("")

        database = project_settings.DATABASES["default"]

        self.assertEqual(database["ENGINE"], "django.db.backends.sqlite3")
        self.assertEqual(
            database["NAME"], str(project_settings.BASE_DIR / "db.sqlite3")
        )

    def test_uses_postgresql_configuration_when_database_url_is_defined(self):
        project_settings = self._reload_settings(
            "postgresql://user:password@aws-0-us-east-1.pooler.supabase.com:6543/postgres"
        )

        database = project_settings.DATABASES["default"]

        self.assertEqual(database["ENGINE"], "django.db.backends.postgresql")
        self.assertEqual(database["HOST"], "aws-0-us-east-1.pooler.supabase.com")
        self.assertEqual(database["PORT"], 6543)
        self.assertEqual(database["CONN_MAX_AGE"], 0)
        self.assertTrue(database["CONN_HEALTH_CHECKS"])
        self.assertIsNone(database["OPTIONS"]["prepare_threshold"])
