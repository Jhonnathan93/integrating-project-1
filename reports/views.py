from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render

from .methods import plot_counts
from .selectors import history_category_counts


@user_passes_test(lambda user: bool(getattr(user, "is_staff", False)))
def reports(request):
    start_date = request.GET.get("fecha_inicio")
    end_date = request.GET.get("fecha_fin")
    if bool(start_date) != bool(end_date):
        return render(request, "reports.html", {"message": "Indica ambas fechas para filtrar el reporte."})
    categories, genres = history_category_counts(start_date=start_date, end_date=end_date)
    plot_counts(values=categories, filename="categories.png", title="Categorías")
    plot_counts(values=genres, filename="genres.png", title="Géneros literarios")
    message = f"Reporte creado con historiales entre {start_date} y {end_date}." if start_date else "Reporte creado con todos los historiales disponibles."
    return render(request, "reports.html", {"message": message})
