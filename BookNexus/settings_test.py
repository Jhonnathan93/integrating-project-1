"""Django settings dedicated to fast, isolated test execution."""

import tempfile
from pathlib import Path

from .settings import *  # noqa: F403

EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"
MEDIA_ROOT = Path(tempfile.gettempdir()) / "booknexus-test-media"
PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]

GOOGLE_BOOKS_API_KEY = ""
GROQ_API_KEY = ""
OPENAI_API_KEY = ""
NEWSLETTER_SENDER_EMAIL = ""
NEWSLETTER_SENDER_PASSWORD = ""
