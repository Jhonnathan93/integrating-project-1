from datetime import timedelta

from django.contrib.auth.models import User
from django.test import SimpleTestCase, TestCase
from django.utils import timezone

from book.models import History
from reports.selectors import _chart_data_from_counts, history_category_counts


class ChartDataSelectorTests(SimpleTestCase):
    def test_chart_data_is_sorted_by_count_then_label(self) -> None:
        chart_data = _chart_data_from_counts(
            values={"Romance": 3, "Fantasía": 5, "Historia": 3}
        )

        self.assertEqual(chart_data["labels"], ["Fantasía", "Historia", "Romance"])
        self.assertEqual(chart_data["values"], [5, 3, 3])


class HistoryCategoryCountsTests(TestCase):
    def test_history_category_counts_splits_and_aggregates_values(self) -> None:
        user = User.objects.create_user(username="reader", password="password")
        History.objects.create(
            user=user,
            books="Dune",
            topics="Fantasy, Space",
            genres="Novel, Science fiction",
        )
        History.objects.create(
            user=user,
            books="Foundation",
            topics="Fantasy",
            genres="Novel",
        )

        categories, genres = history_category_counts()

        self.assertEqual(categories, {"Fantasy": 2, "Space": 1})
        self.assertEqual(genres, {"Novel": 2, "Science fiction": 1})

    def test_history_category_counts_filters_by_complete_date_range(self) -> None:
        user = User.objects.create_user(username="reader", password="password")
        in_range = timezone.now() - timedelta(days=1)
        out_of_range = timezone.now() - timedelta(days=10)
        History.objects.create(
            user=user, books="In range", topics="Fantasy", genres="Novel", date=in_range
        )
        History.objects.create(
            user=user, books="Out of range", topics="History", genres="Essay", date=out_of_range
        )

        categories, genres = history_category_counts(
            start_date=timezone.localdate(in_range),
            end_date=timezone.localdate(),
        )

        self.assertEqual(categories, {"Fantasy": 1})
        self.assertEqual(genres, {"Novel": 1})
