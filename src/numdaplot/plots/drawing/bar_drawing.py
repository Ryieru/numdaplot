"""
Drawing of a BarChart.

.. versionadded:: 0.1.0
"""

# The matplotlib stubs leave the keyword arguments of most drawing methods untyped.
# pyright: reportUnknownMemberType=false

from dataclasses import dataclass
from typing import cast

import numpy
from matplotlib.axes import Axes
from numpy.typing import NDArray

from numdaplot.plots.chart_layer import ChartLayer
from numdaplot.plots.charts.bar_chart import BarChart
from numdaplot.plots.charts.bar_layout import BarLayout
from numdaplot.plots.charts.orientation import Orientation
from numdaplot.plots.data.chart_values import ChartValues
from numdaplot.plots.drawing.default_labels import find_position_label
from numdaplot.plots.drawing.drawn_chart import DrawnChart
from numdaplot.plots.drawing.grid_axes import GridAxes
from numdaplot.plots.drawing.position_axis import place_categories
from numdaplot.plots.drawing.series_colors import choose_series_colors

GROUP_WIDTH = 0.8
HALF = 0.5


@dataclass(frozen=True)
class BarStyle:
	"""
	The look of the bars of one series.

	.. versionadded:: 0.1.0

	Parameters
	----------
	thickness
		The thickness of each bar, a position being 1 wide.
	color_code
		The ``#rrggbb`` code of the bars.

	Examples
	--------
	>>> from numdaplot.plots.drawing.bar_drawing import BarStyle
	>>> BarStyle(0.4, "#1f77b4").thickness
	0.4
	"""

	thickness: float
	color_code: str


@dataclass(frozen=True, eq=False)
class BarSeries:
	"""
	The bars of one series, ready to be drawn.

	.. versionadded:: 0.1.0

	Parameters
	----------
	name
		The name shown in the legend.
	coordinates
		The coordinate of the middle of each bar along the axis of the ``x`` values.
	lengths
		The length of each bar, NaN for a missing value, which draws no bar.
	bases
		Where each bar starts along the axis of the values: 0, or the top of the bars below it when stacked.
	style
		The thickness of the bars and their color code.

	Examples
	--------
	>>> import numpy
	>>> from numdaplot.plots.drawing.bar_drawing import BarSeries, BarStyle
	>>> BarSeries("price", numpy.array([0.0]), numpy.array([12.0]), numpy.array([0.0]), BarStyle(0.8, "#1f77b4")).name
	'price'
	"""

	name: str
	coordinates: NDArray[numpy.float64]
	lengths: NDArray[numpy.float64]
	bases: NDArray[numpy.float64]
	style: BarStyle


@dataclass(frozen=True, eq=False)
class StackTops:
	"""
	Where the next stacked bar starts at each position, above zero and below zero.

	.. versionadded:: 0.1.0

	Parameters
	----------
	positive
		The top of the positive bars already stacked.
	negative
		The bottom of the negative bars already stacked.

	Examples
	--------
	>>> import numpy
	>>> from numdaplot.plots.drawing.bar_drawing import StackTops
	>>> StackTops(numpy.zeros(2), numpy.zeros(2)).positive
	array([0., 0.])
	"""

	positive: NDArray[numpy.float64]
	negative: NDArray[numpy.float64]


def draw_bar_chart(axes: Axes, layer: ChartLayer) -> DrawnChart:
	"""
	Draw each series of a BarChart as bars, one position per ``x`` value.

	A missing value draws no bar. Horizontal bars are drawn from the top, in the order of the rows.

	.. versionadded:: 0.1.0

	Parameters
	----------
	axes
		The matplotlib axes drawn on.
	layer
		A BarChart and its values.

	Returns
	-------
	DrawnChart
		The default labels, where the ``x`` values are, and grid lines across the axis of the values only.

	Raises
	------
	InvalidColorCountError
		When the colors of the chart are not one per series.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> from matplotlib.figure import Figure
	>>> from numdaplot.plots.chart_layer import ChartLayer
	>>> from numdaplot.plots.data.array_values import read_array_values
	>>> from numdaplot.plots.drawing.bar_drawing import draw_bar_chart
	>>> prices = ndp.Array.from_list([12.0, None, 15.5])
	>>> axes = Figure().add_subplot()
	>>> drawn_chart = draw_bar_chart(axes, ChartLayer(ndp.BarChart(), read_array_values(prices, "BarChart")))
	>>> [float(bar.get_height()) for bar in axes.patches]
	[12.0, 15.5]
	"""
	chart = cast(BarChart, layer.chart)
	values = cast(ChartValues, layer.values)
	series_count = len(values.series)
	color_codes = choose_series_colors(chart.colors, series_count)
	is_horizontal = chart.orientation == Orientation.HORIZONTAL
	is_stacked = chart.layout == BarLayout.STACKED
	coordinates = place_categories(axes, values.positions, is_horizontal)
	position_count = len(coordinates)
	stack_tops = StackTops(numpy.zeros(position_count), numpy.zeros(position_count))
	bases = numpy.zeros(position_count)
	thickness = GROUP_WIDTH / series_count
	if is_stacked:
		thickness = GROUP_WIDTH

	for i, series in enumerate(values.series):
		bar_coordinates = find_group_coordinates(coordinates, i, series_count)
		if is_stacked:
			bar_coordinates = coordinates
			bases, stack_tops = stack_bars(series.values, stack_tops)

		bar_style = BarStyle(thickness, color_codes[i])
		bar_series = BarSeries(series.name, bar_coordinates, series.values, bases, bar_style)
		draw_series_bars(axes, bar_series, is_horizontal)

	if is_horizontal:
		axes.invert_yaxis()

	x_label = find_position_label(values.positions)
	drawn_chart = DrawnChart(x_label, values.value_name, is_horizontal, GridAxes.VALUES, None)

	return drawn_chart


def find_group_coordinates(
	coordinates: NDArray[numpy.float64], series_number: int, series_count: int
) -> NDArray[numpy.float64]:
	"""
	Return the middle of the bars of one series when the series are side by side.

	.. versionadded:: 0.1.0

	Parameters
	----------
	coordinates
		The middle of each position.
	series_number
		The number of the series, from 0.
	series_count
		The number of series sharing each position.

	Returns
	-------
	NDArray[numpy.float64]
		The middle of each bar of the series.

	Examples
	--------
	>>> import numpy
	>>> from numdaplot.plots.drawing.bar_drawing import find_group_coordinates
	>>> find_group_coordinates(numpy.array([0.0, 1.0]), 0, 2)
	array([-0.2,  0.8])
	"""
	thickness = GROUP_WIDTH / series_count
	middle_number = series_number + HALF
	group_offset = middle_number * thickness
	group_start = GROUP_WIDTH * HALF
	offset = group_offset - group_start
	shifted_coordinates = coordinates + offset
	# Some versions of the numpy stubs widen the sum of float64 values to any floating type.
	group_coordinates = numpy.asarray(shifted_coordinates, dtype=numpy.float64)

	return group_coordinates


def stack_bars(lengths: NDArray[numpy.float64], stack_tops: StackTops) -> tuple[NDArray[numpy.float64], StackTops]:
	"""
	Return where the bars of a series start when stacked, and the tops of the stacks once they are added.

	Positive values stack above zero and negative values below it. A missing value adds nothing.

	.. versionadded:: 0.1.0

	Parameters
	----------
	lengths
		The values of the series, NaN where a value is missing.
	stack_tops
		The tops of the stacks before this series.

	Returns
	-------
	tuple[NDArray[numpy.float64], StackTops]
		The base of each bar, and the new tops.

	Examples
	--------
	>>> import numpy
	>>> from numdaplot.plots.drawing.bar_drawing import StackTops, stack_bars
	>>> bases, stack_tops = stack_bars(numpy.array([2.0, -1.0]), StackTops(numpy.array([1.0, 1.0]), numpy.zeros(2)))
	>>> bases
	array([1., 0.])
	>>> stack_tops.positive
	array([3., 1.])
	"""
	present_lengths = numpy.nan_to_num(lengths)
	is_positive = present_lengths >= 0
	bases = numpy.where(is_positive, stack_tops.positive, stack_tops.negative)
	tops = bases + present_lengths
	positive_tops = numpy.where(is_positive, tops, stack_tops.positive)
	negative_tops = numpy.where(is_positive, stack_tops.negative, tops)
	new_tops = StackTops(positive_tops, negative_tops)

	return bases, new_tops


def draw_series_bars(axes: Axes, bar_series: BarSeries, is_horizontal: bool) -> None:
	"""
	Draw the bars of one series, except at its missing values.

	.. versionadded:: 0.1.0

	Parameters
	----------
	axes
		The matplotlib axes drawn on.
	bar_series
		The bars of the series.
	is_horizontal
		True to draw horizontal bars.

	Examples
	--------
	>>> import numpy
	>>> from matplotlib.figure import Figure
	>>> from numdaplot.plots.drawing.bar_drawing import BarSeries, BarStyle, draw_series_bars
	>>> axes = Figure().add_subplot()
	>>> bar_style = BarStyle(0.8, "#1f77b4")
	>>> bar_series = BarSeries("price", numpy.arange(2.0), numpy.array([3.0, 4.0]), numpy.zeros(2), bar_style)
	>>> draw_series_bars(axes, bar_series, True)
	>>> [float(bar.get_width()) for bar in axes.patches]
	[3.0, 4.0]
	"""
	is_present = ~numpy.isnan(bar_series.lengths)
	coordinates = bar_series.coordinates[is_present]
	lengths = bar_series.lengths[is_present]
	bases = bar_series.bases[is_present]
	bar_style = bar_series.style
	if is_horizontal:
		axes.barh(
			coordinates,
			lengths,
			height=bar_style.thickness,
			left=bases,
			color=bar_style.color_code,
			label=bar_series.name,
		)
		return

	axes.bar(
		coordinates, lengths, width=bar_style.thickness, bottom=bases, color=bar_style.color_code, label=bar_series.name
	)
