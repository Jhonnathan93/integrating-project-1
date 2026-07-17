from django.contrib.admin.views.decorators import staff_member_required
from django.core.exceptions import ImproperlyConfigured
from django.shortcuts import render
from django.views.decorators.http import require_POST

from .services import newsletter_send


@staff_member_required
@require_POST
def send_email_to_readers(request):
    try:
        newsletter_send()
    except ImproperlyConfigured as error:
        return render(
            request, "email_sent_confirmation.html", {"error": str(error)}, status=503
        )
    return render(request, "email_sent_confirmation.html")
