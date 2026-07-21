from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render
from django.views.decorators.http import require_GET

from .selectors import report_chart_data


@user_passes_test(lambda user: bool(getattr(user, "is_staff", False)))
@require_GET
def reports(request):
    start_date = request.GET.get("fecha_inicio")
    end_date = request.GET.get("fecha_fin")
    if bool(start_date) != bool(end_date):
        return render(
            request,
            "reports.html",
            {
                "message": "Indica ambas fechas para filtrar el informe.",
                "report_available": False,
            },
        )
    chart_data = report_chart_data(start_date=start_date, end_date=end_date)
    message = (
        f"Informe creado con historiales entre {start_date} y {end_date}."
        if start_date
        else "Informe creado con todos los historiales disponibles."
    )
    return render(
        request,
        "reports.html",
        {
            "message": message,
            "report_available": True,
            "chart_data": chart_data,
        },
    )
