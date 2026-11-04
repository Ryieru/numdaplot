"""
Unit tests of the chart settings.

.. versionadded:: 0.1.0
"""

import pytest

from numdaplot.errors.conflicting_settings_error import ConflictingSettingsError
from numdaplot.errors.duplicate_column_error import DuplicateColumnError
from numdaplot.errors.empty_list_error import EmptyListError
from numdaplot.errors.refused_setting_error import RefusedSettingError
from numdaplot.plots.charts.bar_chart import BarChart
from numdaplot.plots.charts.bar_layout import BarLayout
from numdaplot.plots.charts.bin_count import BinCount
from numdaplot.plots.charts.box_chart import BoxChart
from numdaplot.plots.charts.cell_values import CellValues
from numdaplot.plots.charts.chart import Chart
from numdaplot.plots.charts.color_scale import ColorScale
from numdaplot.plots.charts.heatmap_chart import HeatmapChart
from numdaplot.plots.charts.histogram_chart import HistogramChart
from numdaplot.plots.charts.line_chart import LineChart
from numdaplot.plots.charts.line_type import LineType
from numdaplot.plots.charts.marker_shape import MarkerShape
from numdaplot.plots.charts.missing_chart import MissingChart
from numdaplot.plots.charts.missing_map_chart import MissingMapChart
from numdaplot.plots.charts.orientation import Orientation
from numdaplot.plots.charts.outliers import Outliers
from numdaplot.plots.charts.percentages import Percentages
from numdaplot.plots.charts.pie_chart import PieChart
from numdaplot.plots.charts.scatter_chart import ScatterChart
from numdaplot.plots.style.color import Color
from numdaplot.ratios.measure import Measure

Y_COLUMNS = ["price", "cost"]
COLORS = [Color.BLUE, Color.ORANGE]
CHARTS = [
	LineChart(),
	BarChart(),
	ScatterChart(),
	HistogramChart(),
	BoxChart(),
	PieChart(),
	HeatmapChart(),
	MissingChart(),
	MissingMapChart(),
]
DUPLICATE_COLUMNS = ["price", "price"]
DEFAULT_BIN_COUNT = 10


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


def test_histogram_chart_defaults_count_values_in_ten_bins() -> None:
	"""
	Check the defaults of a HistogramChart.

	.. versionadded:: 0.1.0
	"""
	chart = HistogramChart()

	assert chart.columns is None
	assert chart.bins == BinCount(DEFAULT_BIN_COUNT)
	assert chart.measure == Measure.COUNT
	assert chart.colors is None


def test_histogram_chart_keeps_its_own_copy_of_the_lists() -> None:
	"""
	Check that the chart holds copies of columns and colors.

	.. versionadded:: 0.1.0
	"""
	chart = HistogramChart(columns=Y_COLUMNS, colors=COLORS)

	assert chart.columns == Y_COLUMNS
	assert chart.columns is not Y_COLUMNS
	assert chart.colors is not COLORS


def test_histogram_chart_rejects_a_column_twice() -> None:
	"""
	Check that a repeated column raises DuplicateColumnError.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(DuplicateColumnError):
		HistogramChart(columns=DUPLICATE_COLUMNS)


def test_box_chart_defaults_draw_one_box_per_column_with_outliers() -> None:
	"""
	Check the defaults of a BoxChart.

	.. versionadded:: 0.1.0
	"""
	chart = BoxChart()

	assert chart.columns is None
	assert chart.group_by is None
	assert chart.outliers == Outliers.SHOWN
	assert chart.colors is None


def test_box_chart_keeps_its_own_copy_of_the_lists() -> None:
	"""
	Check that the chart holds copies of columns and colors.

	.. versionadded:: 0.1.0
	"""
	chart = BoxChart(columns=Y_COLUMNS, colors=COLORS)

	assert chart.columns is not Y_COLUMNS
	assert chart.colors is not COLORS


def test_box_chart_rejects_empty_colors() -> None:
	"""
	Check that an empty colors list raises EmptyListError.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(EmptyListError):
		BoxChart(colors=[])


def test_pie_chart_defaults_show_the_percentages() -> None:
	"""
	Check the defaults of a PieChart.

	.. versionadded:: 0.1.0
	"""
	chart = PieChart()

	assert chart.labels is None
	assert chart.values is None
	assert chart.percentages == Percentages.SHOWN
	assert chart.colors is None


def test_pie_chart_keeps_its_own_copy_of_the_colors() -> None:
	"""
	Check that the chart holds a copy of colors.

	.. versionadded:: 0.1.0
	"""
	chart = PieChart(colors=COLORS)

	assert chart.colors == COLORS
	assert chart.colors is not COLORS


def test_pie_chart_rejects_empty_colors() -> None:
	"""
	Check that an empty colors list raises EmptyListError.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(EmptyListError):
		PieChart(colors=[])


def test_heatmap_chart_defaults_hide_the_values_on_viridis() -> None:
	"""
	Check the defaults of a HeatmapChart.

	.. versionadded:: 0.1.0
	"""
	chart = HeatmapChart()

	assert chart.columns is None
	assert chart.labels is None
	assert chart.scale == ColorScale.VIRIDIS
	assert chart.values == CellValues.HIDDEN


def test_heatmap_chart_rejects_empty_columns() -> None:
	"""
	Check that an empty columns list raises EmptyListError.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(EmptyListError):
		HeatmapChart(columns=[])


def test_missing_chart_defaults_to_ratios() -> None:
	"""
	Check the default measure of a MissingChart.

	.. versionadded:: 0.1.0
	"""
	chart = MissingChart()

	assert chart.measure == Measure.RATIO
