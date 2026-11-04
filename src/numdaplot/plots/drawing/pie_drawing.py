"""
Drawing of a PieChart.

.. versionadded:: 0.1.0
"""

# The matplotlib stubs leave the keyword arguments of most drawing methods untyped.
# pyright: reportUnknownMemberType=false

import math
from typing import cast

import numpy
from matplotlib.axes import Axes
from matplotlib.colors import to_rgba
from matplotlib.patches import Wedge
from numpy.typing import NDArray

from numdaplot.plots.chart_layer import ChartLayer
from numdaplot.plots.charts.percentages import Percentages
from numdaplot.plots.charts.pie_chart import PieChart
from numdaplot.plots.data.chart_values import ChartValues
from numdaplot.plots.drawing.drawn_chart import DrawnChart
from numdaplot.plots.drawing.grid_axes import GridAxes
from numdaplot.plots.drawing.plot_theme import BACKGROUND_COLOR
from numdaplot.plots.drawing.series_colors import choose_series_colors
from numdaplot.plots.drawing.text_contrast import choose_text_color

# matplotlib measures angles counterclockwise from the right, so 90 degrees is the top of the disc.
TOP_ANGLE = 90.0
SLICE_EDGE_WIDTH = 1.5
PERCENTAGE_FORMAT = "{share:.1%}"
# Share of the radius where the percentage of a slice is written, from the center.
PERCENTAGE_DISTANCE = 0.65
HALF = 0.5
CENTERED = "center"


def draw_pie_chart(axes: Axes, layer: ChartLayer) -> DrawnChart:
	"""
	Draw each value as a slice of a disc, from the top and clockwise, each labeled with its text.

	.. versionadded:: 0.1.0

	Parameters
	----------
	axes
		The matplotlib axes drawn on.
	layer
		A PieChart, its labels and its values.

	Returns
	-------
	DrawnChart
		No default label and no grid lines.

	Raises
	------
	InvalidColorCountError
		When the colors of the chart are not one per slice.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> from matplotlib.figure import Figure
	>>> from numdaplot.plots.chart_layer import ChartLayer
	>>> from numdaplot.plots.data.pie_values import read_pie_values
	>>> from numdaplot.plots.drawing.pie_drawing import draw_pie_chart
	>>> cities = ndp.Array.from_list(["Paris", "Lyon"])
	>>> sales = ndp.Array.from_list([150.0, 50.0])
	>>> shares = ndp.Table.from_arrays({"city": cities, "sales": sales})
	>>> chart = ndp.PieChart(labels="city", values="sales")
	>>> axes = Figure().add_subplot()
	>>> drawn_chart = draw_pie_chart(axes, ChartLayer(chart, read_pie_values(shares, chart)))
	>>> [text.get_text() for text in axes.texts]
	['Paris', 'Lyon', '75.0%', '25.0%']
	"""
	chart = cast(PieChart, layer.chart)
	values = cast(ChartValues, layer.values)
	labels = [str(label) for label in values.positions.values]
	numbers = values.series[0].values
	slice_count = len(labels)
	color_codes = choose_series_colors(chart.colors, slice_count)
	slice_style = {"edgecolor": BACKGROUND_COLOR, "linewidth": SLICE_EDGE_WIDTH}
	axes.pie(
		numbers,
		labels=labels,
		colors=color_codes,
		startangle=TOP_ANGLE,
		counterclock=False,
		wedgeprops=slice_style,
	)
	slices = [patch for patch in axes.patches if isinstance(patch, Wedge)]

	for pie_slice in slices:
		# The labels are written next to the slices, so the legend leaves the slices out.
		pie_slice.set_label("")

	if chart.percentages == Percentages.SHOWN:
		write_percentages(axes, slices, numbers)

	drawn_chart = DrawnChart(None, None, False, GridAxes.NONE, None)

	return drawn_chart


def write_percentages(axes: Axes, slices: list[Wedge], numbers: NDArray[numpy.float64]) -> None:
	"""
	Write the share of each slice inside it, in black or white to stay readable over its color.

	.. versionadded:: 0.1.0

	Parameters
	----------
	axes
		The matplotlib axes drawn on.
	slices
		The slices of the disc, in the order of the values.
	numbers
		The value of each slice, adding up to more than 0.

	Examples
	--------
	>>> import numpy
	>>> from matplotlib.figure import Figure
	>>> from matplotlib.patches import Wedge
	>>> from numdaplot.plots.drawing.pie_drawing import write_percentages
	>>> axes = Figure().add_subplot()
	>>> write_percentages(axes, [Wedge((0.0, 0.0), 1.0, 0.0, 360.0)], numpy.array([4.0]))
	>>> axes.texts[0].get_text()
	'100.0%'
	"""
	total = numbers.sum()
	shares = numbers / total

	for pie_slice, share in zip(slices, shares, strict=True):
		percentage = PERCENTAGE_FORMAT.format(share=share)
		face_color = pie_slice.get_facecolor()
		slice_color = to_rgba(face_color)
		text_color = choose_text_color(slice_color)
		text_x, text_y = find_percentage_place(pie_slice)
		axes.text(
			text_x, text_y, percentage, color=text_color, horizontalalignment=CENTERED, verticalalignment=CENTERED
		)


def find_percentage_place(pie_slice: Wedge) -> tuple[float, float]:
	"""
	Return where the percentage of a slice is written: on its middle angle, partway from the center to the edge.

	.. versionadded:: 0.1.0

	Parameters
	----------
	pie_slice
		A slice of the disc.

	Returns
	-------
	tuple[float, float]
		The horizontal and vertical coordinates.

	Examples
	--------
	>>> from matplotlib.patches import Wedge
	>>> from numdaplot.plots.drawing.pie_drawing import find_percentage_place
	>>> text_x, text_y = find_percentage_place(Wedge((0.0, 0.0), 1.0, 0.0, 180.0))
	>>> round(text_x, 2), round(text_y, 2)
	(0.0, 0.65)
	"""
	angle_sum = pie_slice.theta1 + pie_slice.theta2
	middle_degrees = angle_sum * HALF
	middle_angle = math.radians(middle_degrees)
	distance = pie_slice.r * PERCENTAGE_DISTANCE
	center_x, center_y = pie_slice.center
	cosine = math.cos(middle_angle)
	sine = math.sin(middle_angle)
	x_offset = distance * cosine
	y_offset = distance * sine
	text_x = center_x + x_offset
	text_y = center_y + y_offset

	return text_x, text_y
