from django.test import SimpleTestCase

from .selectors import _chart_data_from_counts


class ChartDataSelectorTests(SimpleTestCase):
    def test_chart_data_is_sorted_by_count_then_label(self) -> None:
        chart_data = _chart_data_from_counts(
            values={"Romance": 3, "Fantasía": 5, "Historia": 3}
        )

        self.assertEqual(chart_data["labels"], ["Fantasía", "Historia", "Romance"])
        self.assertEqual(chart_data["values"], [5, 3, 3])
