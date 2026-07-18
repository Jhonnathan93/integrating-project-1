from collections import Counter
from datetime import date

from book.models import History


def history_category_counts(
    *, start_date: date | None = None, end_date: date | None = None
):
    histories = History.objects.all()
    if start_date and end_date:
        histories = histories.filter(date__date__range=(start_date, end_date))
    categories: Counter[str] = Counter()
    genres: Counter[str] = Counter()
    for history in histories.only("topics", "genres"):
        categories.update(
            value.strip() for value in history.topics.split(",") if value.strip()
        )
        genres.update(
            value.strip() for value in history.genres.split(",") if value.strip()
        )
    return dict(categories), dict(genres)
