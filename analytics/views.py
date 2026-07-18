from django.shortcuts import render
from django.views.decorators.http import require_GET

from .selectors import PERIODS, book_rankings


@require_GET
def top_books(request, period="all"):
    period = period if period in PERIODS else "all"
    top_books, least_books = book_rankings(period=period)
    return render(
        request,
        "top_books.html",
        {"top_books": top_books, "least_books": least_books, "period": period},
    )
