"""
Unit tests of the checks of a chart added to a Plot.

.. versionadded:: 0.1.0
"""

from datetime import date, time

import pytest

import numdaplot as ndp
from numdaplot.plots.chart_layer import ChartLayer
from numdaplot.plots.data.array_values import read_array_values
from numdaplot.plots.data.sample_values import read_sample_values
from numdaplot.plots.data.table_values import read_table_values
from numdaplot.plots.overlay_checks import (
	is_horizontal_bar_chart,
	require_overlay_base,
	require_same_positions,
	require_same_values,
	require_vertical_bars,
)

PRICES = ndp.Array.from_list([12.0, 15.5])
LINE = ChartLayer(ndp.LineChart(), read_array_values(PRICES, "LineChart"))
VERTICAL_BARS = ChartLayer(ndp.BarChart(), read_array_values(PRICES, "BarChart"))
HORIZONTAL_CHART = ndp.BarChart(orientation=ndp.Orientation.HORIZONTAL)
HORIZONTAL_BARS = ChartLayer(HORIZONTAL_CHART, read_array_values(PRICES, "BarChart"))
POINTS = ChartLayer(ndp.ScatterChart(), read_array_values(PRICES, "ScatterChart"))
BOXES = ChartLayer(ndp.BoxChart(), read_sample_values(PRICES, None, None, "BoxChart"))
SHOPS = ndp.Table.from_arrays(
	{
		"city": ndp.Array.from_list(["Paris", "Lyon"]),
		"day": ndp.Array.from_list([date(2026, 1, 1), date(2026, 1, 2)]),
		"sales": PRICES,
	}
)
CITY_BARS = ChartLayer(ndp.BarChart(), read_table_values(SHOPS, "city", ["sales"], "BarChart"))
DATES_OVER_TEXTS_MESSAGE = "A LineChart with dates cannot be added to a Plot with texts"
DAY_LINE = ChartLayer(ndp.LineChart(), read_table_values(SHOPS, "day", ["sales"], "LineChart"))
OVERLAY_HOURS = ndp.Array.from_list([time(8), time(9)])
HOUR_VALUES = read_array_values(OVERLAY_HOURS, "LineChart")
HOUR_LINE = ChartLayer(ndp.LineChart(), HOUR_VALUES)
RIGHT_PRICE_VALUES = read_array_values(PRICES, "LineChart")
RIGHT_LINE = ChartLayer(ndp.LineChart(), RIGHT_PRICE_VALUES, value_axis=ndp.ValueAxis.RIGHT)
TIMES_OVER_NUMBERS_MESSAGE = (
	"A LineChart with times of day on the left axis cannot be added to a Plot with numbers on the left axis."
)


@pytest.mark.parametrize("first_layer", [LINE, VERTICAL_BARS, POINTS])
def test_require_overlay_base_accepts_lines_vertical_bars_and_points(first_layer: ChartLayer) -> None:
	"""
	Check that a Plot of lines, vertical bars or points accepts added charts.

	.. versionadded:: 0.1.0

	Parameters
	----------
	first_layer
		The first chart of the Plot.
	"""
	require_overlay_base(first_layer, "add_line")


def test_require_overlay_base_rejects_another_chart() -> None:
	"""
	Check that a Plot of boxes refuses added charts, naming its chart.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(ndp.RefusedSettingError, match="add_line does not accept a Plot of BoxChart"):
		require_overlay_base(BOXES, "add_line")


def test_require_overlay_base_rejects_horizontal_bars() -> None:
	"""
	Check that a Plot of horizontal bars refuses added charts.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(ndp.RefusedSettingError, match="a Plot of horizontal bars"):
		require_overlay_base(HORIZONTAL_BARS, "add_scatter")


def test_require_vertical_bars_rejects_horizontal_bars() -> None:
	"""
	Check that added bars must be vertical.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(ndp.RefusedSettingError, match="Orientation.HORIZONTAL"):
		require_vertical_bars(HORIZONTAL_CHART, "add_bar")


def test_require_vertical_bars_accepts_vertical_bars() -> None:
	"""
	Check that vertical bars raise nothing.

	.. versionadded:: 0.1.0
	"""
	require_vertical_bars(ndp.BarChart(), "add_bar")


def test_require_same_positions_accepts_the_same_kind() -> None:
	"""
	Check that numbers added over numbers raise nothing.

	.. versionadded:: 0.1.0
	"""
	require_same_positions(VERTICAL_BARS, LINE)


def test_require_same_positions_rejects_another_kind() -> None:
	"""
	Check that dates added over texts raise IncompatibleChartsError naming both kinds.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(
		ndp.IncompatibleChartsError, match="A LineChart with dates cannot be added to a Plot with texts"
	):
		require_same_positions(CITY_BARS, DAY_LINE)


def test_is_horizontal_bar_chart_is_false_for_other_charts() -> None:
	"""
	Check that vertical bars and lines are not horizontal bars.

	.. versionadded:: 0.1.0
	"""
	vertical_answer = is_horizontal_bar_chart(ndp.BarChart())
	line_answer = is_horizontal_bar_chart(ndp.LineChart())

	assert not vertical_answer
	assert not line_answer


def test_require_same_values_accepts_numbers_on_an_axis_of_numbers() -> None:
	"""
	Check that a line of numbers is accepted over bars of numbers.

	.. versionadded:: 0.1.0
	"""
	require_same_values([VERTICAL_BARS], LINE, ndp.ValueAxis.LEFT)


def test_require_same_values_accepts_times_on_the_other_axis() -> None:
	"""
	Check that times of day are accepted on the left when the numbers are on the right.

	.. versionadded:: 0.1.0
	"""
	require_same_values([RIGHT_LINE], HOUR_LINE, ndp.ValueAxis.LEFT)


def test_require_same_values_rejects_times_on_an_axis_of_numbers() -> None:
	"""
	Check that a line of times of day on the axis of numbers raises IncompatibleChartsError.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(ndp.IncompatibleChartsError) as error_info:
		require_same_values([VERTICAL_BARS], HOUR_LINE, ndp.ValueAxis.LEFT)

	message = str(error_info.value)
	assert message == TIMES_OVER_NUMBERS_MESSAGE
