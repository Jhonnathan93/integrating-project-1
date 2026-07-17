from django.shortcuts import render

from .selectors import PERIODS, book_rankings


def top_books(request, period="all"):
    period = period if period in PERIODS else "all"
    top_books, least_books = book_rankings(period=period)
    return render(
        request,
        "top_books.html",
        {"top_books": top_books, "least_books": least_books, "period": period},
    )
