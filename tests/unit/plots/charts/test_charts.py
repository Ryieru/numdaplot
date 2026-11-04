"""
Unit tests of LineChart, BarChart and ScatterChart.

.. versionadded:: 0.1.0
"""

import pytest

from numdaplot.errors.conflicting_settings_error import ConflictingSettingsError
from numdaplot.errors.empty_list_error import EmptyListError
from numdaplot.errors.refused_setting_error import RefusedSettingError
from numdaplot.plots.charts.bar_chart import BarChart
from numdaplot.plots.charts.bar_layout import BarLayout
from numdaplot.plots.charts.chart import Chart
from numdaplot.plots.charts.line_chart import LineChart
from numdaplot.plots.charts.line_type import LineType
from numdaplot.plots.charts.marker_shape import MarkerShape
from numdaplot.plots.charts.orientation import Orientation
from numdaplot.plots.charts.scatter_chart import ScatterChart
from numdaplot.plots.style.color import Color

Y_COLUMNS = ["price", "cost"]
COLORS = [Color.BLUE, Color.ORANGE]
CHARTS = [LineChart(), BarChart(), ScatterChart()]


@pytest.mark.parametrize("chart", CHARTS)
def test_every_chart_is_a_chart(chart: Chart) -> None:
	"""
	Check that each chart inherits Chart.

	.. versionadded:: 0.1.0

	Parameters
	----------
	chart
		A chart with its default settings.
	"""
	assert isinstance(chart, Chart)


def test_line_chart_defaults_draw_solid_lines_without_marker() -> None:
	"""
	Check the defaults of a LineChart.

	.. versionadded:: 0.1.0
	"""
	chart = LineChart()

	assert chart.x is None
	assert chart.y is None
	assert chart.colors is None
	assert chart.line == LineType.SOLID
	assert chart.marker == MarkerShape.NONE


def test_line_chart_keeps_its_own_copy_of_the_lists() -> None:
	"""
	Check that the chart holds copies of y and colors.

	.. versionadded:: 0.1.0
	"""
	chart = LineChart(y=Y_COLUMNS, colors=COLORS)

	assert chart.y == Y_COLUMNS
	assert chart.y is not Y_COLUMNS
	assert chart.colors is not COLORS


def test_line_chart_rejects_empty_y() -> None:
	"""
	Check that an empty y raises EmptyListError.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(EmptyListError):
		LineChart(y=[])


def test_bar_chart_defaults_draw_grouped_vertical_bars() -> None:
	"""
	Check the defaults of a BarChart.

	.. versionadded:: 0.1.0
	"""
	chart = BarChart()

	assert chart.orientation == Orientation.VERTICAL
	assert chart.layout == BarLayout.GROUPED


def test_bar_chart_rejects_empty_colors() -> None:
	"""
	Check that an empty colors list raises EmptyListError.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(EmptyListError):
		BarChart(colors=[])


def test_scatter_chart_defaults_draw_circles() -> None:
	"""
	Check the default marker of a ScatterChart.

	.. versionadded:: 0.1.0
	"""
	chart = ScatterChart()

	assert chart.marker == MarkerShape.CIRCLE


def test_scatter_chart_rejects_a_color_with_color_by() -> None:
	"""
	Check that color and color_by together raise ConflictingSettingsError.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(ConflictingSettingsError):
		ScatterChart(color=Color.RED, color_by="city")


def test_scatter_chart_rejects_points_without_marker() -> None:
	"""
	Check that MarkerShape.NONE raises RefusedSettingError.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(RefusedSettingError):
		ScatterChart(marker=MarkerShape.NONE)
