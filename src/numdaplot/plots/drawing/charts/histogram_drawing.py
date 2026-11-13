"""
Drawing of a HistogramChart.

.. versionadded:: 0.1.0
"""

# The matplotlib stubs leave the keyword arguments of most drawing methods untyped.
# pyright: reportUnknownMemberType=false

import math
from datetime import timedelta
from typing import cast

import numpy
from matplotlib.axes import Axes
from numpy.typing import NDArray

from numdaplot.errors.incompatible_types_error import IncompatibleTypesError
from numdaplot.measures.measure import Measure
from numdaplot.plots.charts.bin_count import BinCount
from numdaplot.plots.charts.bin_width import BinWidth
from numdaplot.plots.charts.histogram_chart import HistogramChart
from numdaplot.plots.data.sample_values import SampleValues, drop_missing_numbers
from numdaplot.plots.drawing.axes.grid_axes import GridAxes
from numdaplot.plots.drawing.axes.time_axis import measures_times, place_hour_ticks
from numdaplot.plots.drawing.axes.whole_numbers import place_whole_ticks
from numdaplot.plots.drawing.colors.colored_parts import ColoredParts
from numdaplot.plots.drawing.colors.series_colors import choose_series_colors
from numdaplot.plots.drawing.drawn_chart import DrawnChart
from numdaplot.plots.drawing.labels.default_labels import find_value_label
from numdaplot.plots.drawing.plot_theme import BACKGROUND_COLOR
from numdaplot.plots.layers.chart_layer import ChartLayer
from numdaplot.types.type import Type

CHART_NAME = "HistogramChart"
MEASURE_LABELS = {
	Measure.COUNT: "Count",
	Measure.RATIO: "Ratio",
}
SINGLE_OPACITY = 1.0
OVERLAID_OPACITY = 0.5
BIN_EDGE_WIDTH = 0.8
# Each bar starts at the left edge of its bin.
BIN_ALIGNMENT = "edge"
DEFAULT_BIN_COUNT = 10
HOURS_PER_DAY = 24
DAY_EDGE_COUNT = HOURS_PER_DAY + 1
ONE_HOUR = timedelta(hours=1)
NUMBER_WIDTH_TYPE = Type.FLOAT64
DURATION_WIDTH_TYPE = Type.DURATION
WIDTH_OPERATION = "BinWidth"


def draw_histogram_chart(axes: Axes, layer: ChartLayer) -> DrawnChart:
	"""
	Draw how many values of each column fall in each bin, the columns sharing the same bins.

	Several columns are drawn over each other, half transparent. Missing values are left out.

	.. versionadded:: 0.1.0
	.. versionchanged:: 0.2.0
		Labels the axis of several series ``Value``, their names staying in the default title.

	Parameters
	----------
	axes
		The matplotlib axes drawn on.
	layer
		A HistogramChart and its columns.

	Returns
	-------
	DrawnChart
		The single column as default label of the values, ``"Count"`` or ``"Ratio"`` as label of the other axis,
		and grid lines across that axis only.

	Raises
	------
	InvalidColorCountError
		When the colors of the chart are not one per column.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> from matplotlib.figure import Figure
	>>> from numdaplot.plots.layers.chart_layer import ChartLayer
	>>> from numdaplot.plots.data.sample_values import read_sample_values
	>>> from numdaplot.plots.drawing.charts.histogram_drawing import draw_histogram_chart
	>>> prices = ndp.Array.from_list([12.0, 13.0, 17.0, None])
	>>> axes = Figure().add_subplot()
	>>> samples = read_sample_values(prices, None, None, "HistogramChart")
	>>> layer = ChartLayer(ndp.HistogramChart(bins=ndp.BinWidth(5.0)), samples)
	>>> drawn_chart = draw_histogram_chart(axes, layer)
	>>> [float(bar.get_height()) for bar in axes.patches]
	[2.0, 1.0]
	"""
	chart = cast(HistogramChart, layer.chart)
	values = cast(SampleValues, layer.values)
	series_count = len(values.series)
	color_codes = choose_series_colors(chart.colors, series_count, CHART_NAME, ColoredParts.SERIES)
	samples = [drop_missing_numbers(series.values) for series in values.series]
	all_numbers = numpy.concatenate(samples)
	bin_edges = find_bin_edges(all_numbers, chart.bins, values.value_type)
	bin_starts = bin_edges[:-1]
	bin_widths = numpy.diff(bin_edges)
	opacity = SINGLE_OPACITY
	if series_count > 1:
		opacity = OVERLAID_OPACITY

	bin_counts = list[NDArray[numpy.float64]]()

	for i, series in enumerate(values.series):
		weights = find_bin_weights(samples[i], chart.measure)
		counts, _ = numpy.histogram(samples[i], bins=bin_edges, weights=weights)
		series_counts = numpy.asarray(counts, dtype=numpy.float64)
		axes.bar(
			bin_starts,
			series_counts,
			width=bin_widths,
			align=BIN_ALIGNMENT,
			color=color_codes[i],
			alpha=opacity,
			label=series.name,
			edgecolor=BACKGROUND_COLOR,
			linewidth=BIN_EDGE_WIDTH,
		)
		bin_counts.append(series_counts)

	all_counts = numpy.concatenate(bin_counts)
	place_whole_ticks(axes.yaxis, all_counts)

	is_time = measures_times(values.value_type)
	if is_time:
		place_hour_ticks(axes.xaxis, bin_edges)

	measure_label = MEASURE_LABELS[chart.measure]
	value_label = find_value_label(values)
	drawn_chart = DrawnChart(value_label, measure_label, False, GridAxes.VALUES, None, x_title_name=values.value_name)

	return drawn_chart


def require_bins_on_values(bins: BinCount | BinWidth | None, value_type: Type) -> None:
	"""
	Check that the width of the bins of a histogram is a number for numbers and a duration for times of day.

	.. versionadded:: 0.1.0

	Parameters
	----------
	bins
		The bins of the HistogramChart, None for the default ones.
	value_type
		The type of the values drawn.

	Raises
	------
	IncompatibleTypesError
		When a number gives the width of bins of times of day, or a duration the width of bins of numbers.

	Examples
	--------
	>>> from datetime import timedelta
	>>> import numdaplot as ndp
	>>> from numdaplot.plots.drawing.charts.histogram_drawing import require_bins_on_values
	>>> try:
	... 	require_bins_on_values(ndp.BinWidth(timedelta(hours=1)), ndp.Type.FLOAT64)
	... except ndp.IncompatibleTypesError as error:
	... 	print(error)
	Cannot apply BinWidth to DURATION and FLOAT64.
	"""
	if not isinstance(bins, BinWidth):
		return

	is_time = measures_times(value_type)
	is_duration = isinstance(bins.width, timedelta)
	if is_duration == is_time:
		return

	width_type = NUMBER_WIDTH_TYPE
	if is_duration:
		width_type = DURATION_WIDTH_TYPE

	raise IncompatibleTypesError(WIDTH_OPERATION, [width_type.name, value_type.name])


def find_bin_edges(
	numbers: NDArray[numpy.float64], bins: BinCount | BinWidth | None, value_type: Type
) -> NDArray[numpy.float64]:
	"""
	Return the edges of the bins of a histogram.

	.. versionadded:: 0.1.0

	Parameters
	----------
	numbers
		Every number drawn, of every column, none missing, a time of day being its hours since midnight.
	bins
		The number of bins, spread from the smallest to the largest number, or their width, checked against the
		values. None gives 10 bins for numbers and one bin per hour from 00:00 to 24:00 for times of day.
	value_type
		The type of the values drawn.

	Returns
	-------
	NDArray[numpy.float64]
		One edge more than there are bins, in hours for times of day.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> import numpy
	>>> from numdaplot.plots.drawing.charts.histogram_drawing import find_bin_edges
	>>> find_bin_edges(numpy.array([12.0, 20.0]), ndp.BinCount(4), ndp.Type.FLOAT64)
	array([12., 14., 16., 18., 20.])
	>>> len(find_bin_edges(numpy.array([8.5]), None, ndp.Type.TIME))
	25
	"""
	is_time = measures_times(value_type)
	uses_day_edges = bins is None and is_time
	if uses_day_edges:
		day_edges = numpy.arange(DAY_EDGE_COUNT, dtype=numpy.float64)
		return day_edges

	if bins is None:
		bins = BinCount(DEFAULT_BIN_COUNT)

	if isinstance(bins, BinWidth):
		width = read_width_hours(bins)
		width_edges = find_width_edges(numbers, width)
		return width_edges

	count_edges = numpy.histogram_bin_edges(numbers, bins=bins.count)

	return count_edges


def read_width_hours(bins: BinWidth) -> float:
	"""
	Return the width of bins as a number, a duration being counted in hours.

	.. versionadded:: 0.1.0

	Parameters
	----------
	bins
		The width of the bins.

	Returns
	-------
	float
		The width of bins of numbers, or the hours of a duration.

	Examples
	--------
	>>> from datetime import timedelta
	>>> import numdaplot as ndp
	>>> from numdaplot.plots.drawing.charts.histogram_drawing import read_width_hours
	>>> read_width_hours(ndp.BinWidth(timedelta(minutes=30))), read_width_hours(ndp.BinWidth(2.5))
	(0.5, 2.5)
	"""
	if isinstance(bins.width, timedelta):
		width_hours = bins.width / ONE_HOUR
		return width_hours

	return bins.width


def find_width_edges(numbers: NDArray[numpy.float64], width: float) -> NDArray[numpy.float64]:
	"""
	Return the edges of bins of a given width, each edge being a multiple of the width.

	The first edge is the largest multiple not above the smallest number, and the bins go on until the largest
	number. Without numbers, a single bin starts at 0.

	.. versionadded:: 0.1.0

	Parameters
	----------
	numbers
		Every number drawn, none missing.
	width
		The width of each bin, above 0.

	Returns
	-------
	NDArray[numpy.float64]
		The edges, at least two.

	Examples
	--------
	>>> import numpy
	>>> from numdaplot.plots.drawing.charts.histogram_drawing import find_width_edges
	>>> find_width_edges(numpy.array([12.0, 21.0]), 5.0)
	array([10., 15., 20., 25.])
	"""
	smallest_number = 0.0
	largest_number = 0.0
	number_count = len(numbers)
	if number_count > 0:
		smallest_number = float(numbers.min())
		largest_number = float(numbers.max())

	first_width_count = math.floor(smallest_number / width)
	first_edge = first_width_count * width
	covered_widths = (largest_number - first_edge) / width
	bin_count = math.ceil(covered_widths)
	bin_count = max(bin_count, 1)
	edge_count = bin_count + 1
	edge_numbers = numpy.arange(edge_count, dtype=numpy.float64)
	edge_offsets = edge_numbers * width
	shifted_offsets = first_edge + edge_offsets
	# Some versions of the numpy stubs widen the sum of float64 values to any floating type.
	edges = numpy.asarray(shifted_offsets, dtype=numpy.float64)

	return edges


def find_bin_weights(numbers: NDArray[numpy.float64], measure: Measure) -> NDArray[numpy.float64] | None:
	"""
	Return how much each number weighs in its bin.

	.. versionadded:: 0.1.0

	Parameters
	----------
	numbers
		The numbers of one column, none missing.
	measure
		``Measure.COUNT`` to count the numbers, ``Measure.RATIO`` for their share of the column.

	Returns
	-------
	NDArray[numpy.float64] or None
		None to count each number once, or one share per number, the shares adding up to 1.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> import numpy
	>>> from numdaplot.plots.drawing.charts.histogram_drawing import find_bin_weights
	>>> find_bin_weights(numpy.array([3.0, 5.0, 8.0, 9.0]), ndp.Measure.RATIO)
	array([0.25, 0.25, 0.25, 0.25])
	"""
	number_count = len(numbers)
	is_counted = measure == Measure.COUNT
	has_no_numbers = number_count == 0
	weighs_one = is_counted or has_no_numbers
	if weighs_one:
		return None

	share = 1 / number_count
	weights = numpy.full(number_count, share)

	return weights
