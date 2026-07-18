from collections import Counter
from datetime import date
from typing import TypedDict

from book.models import History


class ChartData(TypedDict):
    labels: list[str]
    values: list[int]


class ReportsChartData(TypedDict):
    categories: ChartData
    genres: ChartData


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


def report_chart_data(
    *, start_date: date | None = None, end_date: date | None = None
) -> ReportsChartData:
    categories, genres = history_category_counts(
        start_date=start_date, end_date=end_date
    )
    return {
        "categories": _chart_data_from_counts(values=categories),
        "genres": _chart_data_from_counts(values=genres),
    }


def _chart_data_from_counts(*, values: dict[str, int]) -> ChartData:
    sorted_items = sorted(values.items(), key=lambda item: (-item[1], item[0]))
    return {
        "labels": [label for label, _ in sorted_items],
        "values": [count for _, count in sorted_items],
    }
