"""
Unit tests of the drawing of a LineChart.

.. versionadded:: 0.1.0
"""

# The matplotlib stubs leave the keyword arguments of most drawing methods untyped.
# pyright: reportUnknownMemberType=false

import numpy
from matplotlib.figure import Figure

import numdaplot as ndp
from numdaplot.plots.chart_layer import ChartLayer
from numdaplot.plots.data.table_values import read_table_values
from numdaplot.plots.drawing.grid_axes import GridAxes
from numdaplot.plots.drawing.line_drawing import draw_line_chart

DAYS = ndp.Array.from_list([1, 2, 3])
PRICES = ndp.Array.from_list([12.0, 15.5, 14.0])
COSTS = ndp.Array.from_list([8.0, None, 9.0])
SALES = ndp.Table.from_arrays({"day": DAYS, "price": PRICES, "cost": COSTS})
CHART = ndp.LineChart(
	x="day",
	y=["price", "cost"],
	colors=[ndp.Color.RED, ndp.CustomColor("#ff8800")],
	line=ndp.LineType.DASHED,
	marker=ndp.MarkerShape.SQUARE,
)
VALUES = read_table_values(SALES, "day", ["price", "cost"], "LineChart")
LAYER = ChartLayer(CHART, VALUES)
EXPECTED_COLORS = ["#d62728", "#ff8800"]
EXPECTED_Y_LABEL = "price, cost"


def test_draw_line_chart_draws_one_line_per_series_with_its_name() -> None:
	"""
	Check that each y column is a line labeled with its name.

	.. versionadded:: 0.1.0
	"""
	axes = Figure().add_subplot()

	draw_line_chart(axes, LAYER)

	labels = [line.get_label() for line in axes.lines]
	assert labels == ["price", "cost"]


def test_draw_line_chart_draws_the_look_of_the_chart() -> None:
	"""
	Check the colors, the line type and the marker of the lines.

	.. versionadded:: 0.1.0
	"""
	axes = Figure().add_subplot()

	draw_line_chart(axes, LAYER)

	colors = [line.get_color() for line in axes.lines]
	first_line = axes.lines[0]
	assert colors == EXPECTED_COLORS
	assert first_line.get_linestyle() == "--"
	assert first_line.get_marker() == "s"


def test_draw_line_chart_breaks_the_line_at_a_missing_value() -> None:
	"""
	Check that a missing value is drawn as NaN, which breaks the line.

	.. versionadded:: 0.1.0
	"""
	axes = Figure().add_subplot()

	draw_line_chart(axes, LAYER)

	cost_values = numpy.asarray(axes.lines[1].get_ydata(), dtype=numpy.float64)
	missing = numpy.isnan(cost_values).tolist()
	assert missing == [False, True, False]


def test_draw_line_chart_gives_the_default_labels() -> None:
	"""
	Check that the x column names the axis of the positions, and that several series all name the values.

	.. versionadded:: 0.1.0
	"""
	axes = Figure().add_subplot()

	drawn_chart = draw_line_chart(axes, LAYER)

	assert drawn_chart.x_label == "day"
	assert drawn_chart.y_label == EXPECTED_Y_LABEL
	assert drawn_chart.grid_axes == GridAxes.BOTH
	assert not drawn_chart.x_on_vertical_axis
