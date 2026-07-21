"""Django settings dedicated to fast, isolated test execution."""

import tempfile
from pathlib import Path

from . import settings as base_settings

for setting_name in dir(base_settings):
    if setting_name.isupper():
        globals()[setting_name] = getattr(base_settings, setting_name)

EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"
MEDIA_ROOT = Path(tempfile.gettempdir()) / "booknexus-test-media"
PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]

GOOGLE_BOOKS_API_KEY = ""
GROQ_API_KEY = ""
OPENAI_API_KEY = ""
NEWSLETTER_SENDER_EMAIL = ""
NEWSLETTER_SENDER_PASSWORD = ""
