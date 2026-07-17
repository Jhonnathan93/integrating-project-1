import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

from book.models import Reader

NEWSLETTER_SUBJECT = "BookNexus - Newsletter"
NEWSLETTER_BODY = "<html><body><img src='https://github.com/jhothinnan/Images/blob/main/Newsletter.png?raw=true' alt='Newsletter'></body></html>"


def newsletter_send() -> int:
    sender_email = getattr(settings, "NEWSLETTER_SENDER_EMAIL", "")
    password = getattr(settings, "NEWSLETTER_SENDER_PASSWORD", "")
    if not sender_email or not password:
        raise ImproperlyConfigured("Configura NEWSLETTER_SENDER_EMAIL y NEWSLETTER_SENDER_PASSWORD.")
    readers = Reader.objects.exclude(email="").values_list("email", flat=True)
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        for recipient in readers:
            message = MIMEMultipart("alternative")
            message["Subject"], message["From"], message["To"] = NEWSLETTER_SUBJECT, sender_email, recipient
            message.attach(MIMEText(NEWSLETTER_BODY, "html"))
            server.sendmail(sender_email, recipient, message.as_string())
    return len(readers)
