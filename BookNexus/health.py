"""Health endpoint used by orchestration and container smoke tests."""

from django.db import DatabaseError, connections
from django.http import JsonResponse
from django.views.decorators.http import require_GET


@require_GET
def health(request):
    """Return readiness status after verifying the default database connection."""

    try:
        with connections["default"].cursor() as cursor:
            cursor.execute("SELECT 1")
            cursor.fetchone()
    except DatabaseError:
        return JsonResponse({"status": "unavailable"}, status=503)
    return JsonResponse({"status": "ok"})
