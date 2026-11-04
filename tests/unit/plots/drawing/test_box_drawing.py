"""
Unit tests of the drawing of a BoxChart.

.. versionadded:: 0.1.0
"""

# The matplotlib stubs leave the keyword arguments of most drawing methods untyped.
# pyright: reportUnknownMemberType=false

import numpy
import pandas
from matplotlib.colors import to_rgba
from matplotlib.figure import Figure
from matplotlib.patches import PathPatch

import numdaplot as ndp
from numdaplot.plots.chart_layer import ChartLayer
from numdaplot.plots.data.sample_values import read_sample_values
from numdaplot.plots.drawing.box_drawing import OUTLIER_MARKER, BoxLook, draw_box_chart, draw_boxes, sort_groups
from numdaplot.plots.drawing.grid_axes import GridAxes
from numdaplot.plots.drawing.series_colors import COLOR_CODES

CHART_NAME = "BoxChart"
FLATS_FRAME = pandas.DataFrame(
	{
		"city": ["Pau", "Lyon", None, "Pau", "Lyon"],
		"2025": [12.0, 9.5, 30.0, 14.0, 10.0],
		"2026": [13.0, 10.5, 31.0, 15.0, None],
	}
)
FLATS = ndp.Table.from_pandas(FLATS_FRAME)
TWO_COLUMNS = ["2025", "2026"]
EXPECTED_GROUPS = ["Lyon", "Pau"]
EXPECTED_LIMITS = [-0.5, 1.5]
OUTLIER_SAMPLE = numpy.array([12.0, 13.0, 14.0, 13.5, 12.5, 60.0])
BOX_LOOK = BoxLook("#1f77b4", 0.5, True, None)
HIDDEN_OUTLIERS_LOOK = BoxLook("#1f77b4", 0.5, False, None)
SINGLE_COORDINATE = numpy.array([0.0])
RED_RGBA = to_rgba(COLOR_CODES[ndp.Color.RED])
GREEN_RGBA = to_rgba(COLOR_CODES[ndp.Color.GREEN])
GROUPS_WITH_GAPS = numpy.array(["Pau", None, "Lyon", "Pau"], dtype=object)


def build_layer(chart: ndp.BoxChart) -> ChartLayer:
	"""
	Return a BoxChart of the flats with its values.

	.. versionadded:: 0.1.0

	Parameters
	----------
	chart
		The chart drawn.

	Returns
	-------
	ChartLayer
		The chart, its columns and their groups.
	"""
	samples = read_sample_values(FLATS, chart.columns, chart.group_by, CHART_NAME)
	layer = ChartLayer(chart, samples)

	return layer


def count_boxes(figure: Figure) -> int:
	"""
	Return the number of boxes drawn on the first axes of a figure.

	.. versionadded:: 0.1.0

	Parameters
	----------
	figure
		A figure with boxes.

	Returns
	-------
	int
		The number of boxes.
	"""
	boxes = [patch for patch in figure.axes[0].patches if isinstance(patch, PathPatch)]
	box_count = len(boxes)

	return box_count


def read_tick_labels(figure: Figure) -> list[str]:
	"""
	Return the labels of the horizontal ticks of the first axes of a figure.

	.. versionadded:: 0.1.0

	Parameters
	----------
	figure
		A figure with boxes.

	Returns
	-------
	list[str]
		The text of each tick.
	"""
	tick_labels = figure.axes[0].get_xticklabels()
	label_texts = [label.get_text() for label in tick_labels]

	return label_texts


def test_draw_box_chart_draws_one_box_per_column() -> None:
	"""
	Check that each column gets a box at a position labeled with its name, with half a position of margin.

	.. versionadded:: 0.1.0
	"""
	figure = Figure()
	axes = figure.add_subplot()

	drawn_chart = draw_box_chart(axes, build_layer(ndp.BoxChart(columns=TWO_COLUMNS)))

	box_count = count_boxes(figure)
	label_texts = read_tick_labels(figure)
	limits = list(axes.get_xlim())
	assert box_count == 2
	assert label_texts == TWO_COLUMNS
	assert limits == EXPECTED_LIMITS
	assert drawn_chart.grid_axes == GridAxes.VALUES


def test_draw_box_chart_draws_the_columns_side_by_side_in_each_group() -> None:
	"""
	Check that each group in alphabetical order gets one box per column, the missing group left out.

	.. versionadded:: 0.1.0
	"""
	figure = Figure()
	axes = figure.add_subplot()
	chart = ndp.BoxChart(columns=TWO_COLUMNS, group_by="city")

	drawn_chart = draw_box_chart(axes, build_layer(chart))

	box_count = count_boxes(figure)
	label_texts = read_tick_labels(figure)
	_, legend_labels = axes.get_legend_handles_labels()
	assert box_count == 4
	assert label_texts == EXPECTED_GROUPS
	assert legend_labels == TWO_COLUMNS
	assert drawn_chart.x_label == "city"


def test_draw_box_chart_names_the_values_after_a_single_column() -> None:
	"""
	Check that a single column gives the default label of the values.

	.. versionadded:: 0.1.0
	"""
	axes = Figure().add_subplot()

	drawn_chart = draw_box_chart(axes, build_layer(ndp.BoxChart(columns=["2025"])))

	assert drawn_chart.y_label == "2025"


def test_draw_box_chart_paints_each_column_in_its_color() -> None:
	"""
	Check that the colors of the chart fill the boxes of each column.

	.. versionadded:: 0.1.0
	"""
	figure = Figure()
	axes = figure.add_subplot()
	chart = ndp.BoxChart(columns=TWO_COLUMNS, colors=[ndp.Color.RED, ndp.Color.GREEN])

	draw_box_chart(axes, build_layer(chart))

	boxes = [patch for patch in axes.patches if isinstance(patch, PathPatch)]
	face_colors = [box.get_facecolor() for box in boxes]
	expected_colors = [RED_RGBA, GREEN_RGBA]
	assert face_colors == expected_colors


def test_draw_boxes_draws_the_outliers_when_shown() -> None:
	"""
	Check that a value far from the others is drawn as a point.

	.. versionadded:: 0.1.0
	"""
	axes = Figure().add_subplot()

	draw_boxes(axes, [OUTLIER_SAMPLE], SINGLE_COORDINATE, BOX_LOOK)

	outlier_points = [line for line in axes.lines if line.get_marker() == OUTLIER_MARKER]
	outlier_data = outlier_points[0].get_ydata()
	outlier_values = numpy.asarray(outlier_data).tolist()
	assert outlier_values == [60.0]


def test_draw_boxes_hides_the_outliers_when_hidden() -> None:
	"""
	Check that no outlier point is drawn when hidden.

	.. versionadded:: 0.1.0
	"""
	axes = Figure().add_subplot()

	draw_boxes(axes, [OUTLIER_SAMPLE], SINGLE_COORDINATE, HIDDEN_OUTLIERS_LOOK)

	point_lines = [line for line in axes.lines if line.get_marker() == OUTLIER_MARKER]
	assert point_lines == []


def test_draw_boxes_draws_nothing_without_values() -> None:
	"""
	Check that a sample of missing values only draws no box.

	.. versionadded:: 0.1.0
	"""
	axes = Figure().add_subplot()
	empty_sample = numpy.array([numpy.nan])

	draw_boxes(axes, [empty_sample], SINGLE_COORDINATE, BOX_LOOK)

	patch_count = len(axes.patches)
	assert patch_count == 0


def test_sort_groups_gives_each_group_once_in_alphabetical_order() -> None:
	"""
	Check that groups are unique, sorted, and without the missing one.

	.. versionadded:: 0.1.0
	"""
	group_names = sort_groups(GROUPS_WITH_GAPS)

	assert group_names.tolist() == EXPECTED_GROUPS
