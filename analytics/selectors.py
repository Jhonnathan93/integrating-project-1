from datetime import timedelta

from django.db.models import Count
from django.utils import timezone

from book.models import Book

PERIODS = {"week": timedelta(weeks=1), "month": timedelta(days=30), "6months": timedelta(days=180), "year": timedelta(days=365)}


def book_rankings(*, period: str):
    queryset = Book.objects.all()
    if period in PERIODS:
        queryset = queryset.filter(dateAdded__gte=timezone.now() - PERIODS[period])
    grouped = queryset.values("title", "isbn").annotate(book_count=Count("id"))
    return grouped.order_by("-book_count", "title")[:5], grouped.order_by("book_count", "title")[:5]
