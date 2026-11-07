"""
Drawing of a BoxChart.

.. versionadded:: 0.1.0
"""

# The matplotlib stubs leave the keyword arguments of most drawing methods untyped.
# pyright: reportUnknownMemberType=false

from dataclasses import dataclass
from typing import Any, cast

import numpy
import pandas
from matplotlib.axes import Axes
from numpy.typing import NDArray

from numdaplot.plots.chart_layer import ChartLayer
from numdaplot.plots.charts.box_chart import BoxChart
from numdaplot.plots.charts.outliers import Outliers
from numdaplot.plots.data.chart_values import Positions, Series
from numdaplot.plots.data.position_kind import PositionKind
from numdaplot.plots.data.sample_values import SampleValues, drop_missing_numbers
from numdaplot.plots.drawing.bar_drawing import GROUP_WIDTH, find_group_coordinates
from numdaplot.plots.drawing.default_labels import COLUMN_LABEL
from numdaplot.plots.drawing.drawn_chart import DrawnChart
from numdaplot.plots.drawing.grid_axes import GridAxes
from numdaplot.plots.drawing.plot_theme import BACKGROUND_COLOR
from numdaplot.plots.drawing.position_axis import place_categories
from numdaplot.plots.drawing.series_colors import choose_series_colors
from numdaplot.plots.drawing.time_axis import measures_times, place_hour_ticks

# Share of its place a box fills, leaving a gap between two boxes side by side.
BOX_SHARE = 0.8
# Width of a box alone at its position, a position being 1 wide.
COLUMN_BOX_WIDTH = 0.5
HALF_POSITION = 0.5
MEDIAN_LINE_WIDTH = 1.5
OUTLIER_MARKER = "o"
OUTLIER_SIZE = 4.0
TEXT_DTYPE = numpy.dtype(object)


@dataclass(frozen=True)
class BoxLook:
	"""
	The look shared by the boxes of one column.

	.. versionadded:: 0.1.0

	Parameters
	----------
	color_code
		The ``#rrggbb`` code of the boxes.
	width
		The width of each box, a position being 1 wide.
	shows_outliers
		True to draw the outliers.
	label
		The name shown in the legend, or None to leave the boxes out of it.

	Examples
	--------
	>>> from numdaplot.plots.drawing.box_drawing import BoxLook
	>>> BoxLook("#1f77b4", 0.8, True, None).width
	0.8
	"""

	color_code: str
	width: float
	shows_outliers: bool
	label: str | None


def draw_box_chart(axes: Axes, layer: ChartLayer) -> DrawnChart:
	"""
	Draw the values of each column as a box, one per column, or one per column side by side in each group.

	Each position is 1 wide, with half a position of margin at both ends, as for bars.

	.. versionadded:: 0.1.0

	Parameters
	----------
	axes
		The matplotlib axes drawn on.
	layer
		A BoxChart, its columns and their groups.

	Returns
	-------
	DrawnChart
		The ``group_by`` column and the single column as default labels, and grid lines across the axis of the
		values only, labeled ``HH:MM`` for times of day.

	Raises
	------
	InvalidColorCountError
		When the colors of the chart are not one per column.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> from matplotlib.figure import Figure
	>>> from numdaplot.plots.chart_layer import ChartLayer
	>>> from numdaplot.plots.data.sample_values import read_sample_values
	>>> from numdaplot.plots.drawing.box_drawing import draw_box_chart
	>>> prices = ndp.Array.from_list([[12.0, 9.5], [14.0, 10.0], [13.5, 8.0]])
	>>> axes = Figure().add_subplot()
	>>> layer = ChartLayer(ndp.BoxChart(), read_sample_values(prices, None, None, "BoxChart"))
	>>> drawn_chart = draw_box_chart(axes, layer)
	>>> [label.get_text() for label in axes.get_xticklabels()]
	['0', '1']
	"""
	chart = cast(BoxChart, layer.chart)
	values = cast(SampleValues, layer.values)
	series_count = len(values.series)
	color_codes = choose_series_colors(chart.colors, series_count)
	shows_outliers = chart.outliers == Outliers.SHOWN
	if values.groups is None:
		position_count = draw_column_boxes(axes, values.series, color_codes, shows_outliers)
	else:
		position_count = draw_group_boxes(axes, values, color_codes, shows_outliers)

	last_edge = position_count - HALF_POSITION
	axes.set_xlim(-HALF_POSITION, last_edge)

	is_time = measures_times(values.value_type)
	if is_time:
		series_values = [series.values for series in values.series]
		hours = numpy.concatenate(series_values)
		place_hour_ticks(axes.yaxis, hours)

	x_label = COLUMN_LABEL
	if values.group_name is not None:
		x_label = values.group_name

	drawn_chart = DrawnChart(x_label, values.value_name, False, GridAxes.VALUES, None)

	return drawn_chart


def draw_column_boxes(axes: Axes, series_list: list[Series], color_codes: list[str], shows_outliers: bool) -> int:
	"""
	Draw one box per column, each at its own position labeled with the column name.

	.. versionadded:: 0.1.0

	Parameters
	----------
	axes
		The matplotlib axes drawn on.
	series_list
		The columns drawn.
	color_codes
		One ``#rrggbb`` code per column.
	shows_outliers
		True to draw the outliers.

	Returns
	-------
	int
		The number of positions, one per column.

	Examples
	--------
	>>> import numpy
	>>> from matplotlib.figure import Figure
	>>> from numdaplot.plots.data.chart_values import Series
	>>> from numdaplot.plots.drawing.box_drawing import draw_column_boxes
	>>> axes = Figure().add_subplot()
	>>> draw_column_boxes(axes, [Series("price", numpy.array([1.0, 2.0, 4.0]))], ["#1f77b4"], True)
	1
	>>> [label.get_text() for label in axes.get_xticklabels()]
	['price']
	"""
	column_names = [series.name for series in series_list]
	name_values = numpy.array(column_names, dtype=TEXT_DTYPE)
	positions = Positions(PositionKind.TEXTS, name_values, None)
	coordinates = place_categories(axes, positions, False)

	for i, series in enumerate(series_list):
		samples = [series.values]
		box_coordinates = coordinates[i : i + 1]
		box_look = BoxLook(color_codes[i], COLUMN_BOX_WIDTH, shows_outliers, None)
		draw_boxes(axes, samples, box_coordinates, box_look)

	position_count = len(coordinates)

	return position_count


def draw_group_boxes(axes: Axes, values: SampleValues, color_codes: list[str], shows_outliers: bool) -> int:
	"""
	Draw one position per group in alphabetical order, with the boxes of the columns side by side.

	Rows whose group is missing are left out. The columns are named in the legend.

	.. versionadded:: 0.1.0

	Parameters
	----------
	axes
		The matplotlib axes drawn on.
	values
		The columns, the group of each row and the ``group_by`` column.
	color_codes
		One ``#rrggbb`` code per column.
	shows_outliers
		True to draw the outliers.

	Returns
	-------
	int
		The number of positions, one per group.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> from matplotlib.figure import Figure
	>>> from numdaplot.plots.data.sample_values import read_sample_values
	>>> from numdaplot.plots.drawing.box_drawing import draw_group_boxes
	>>> cities = ndp.Array.from_list(["Paris", "Lyon", "Paris", "Lyon"])
	>>> prices = ndp.Array.from_list([12.0, 9.5, 14.0, 10.0])
	>>> flats = ndp.Table.from_arrays({"city": cities, "price": prices})
	>>> axes = Figure().add_subplot()
	>>> draw_group_boxes(axes, read_sample_values(flats, ["price"], "city", "BoxChart"), ["#1f77b4"], True)
	2
	>>> [label.get_text() for label in axes.get_xticklabels()]
	['Lyon', 'Paris']
	"""
	groups = cast(NDArray[Any], values.groups)
	group_names = sort_groups(groups)
	positions = Positions(PositionKind.TEXTS, group_names, values.group_name)
	coordinates = place_categories(axes, positions, False)
	series_count = len(values.series)
	slot_width = GROUP_WIDTH / series_count
	box_width = slot_width * BOX_SHARE

	for i, series in enumerate(values.series):
		box_coordinates = find_group_coordinates(coordinates, i, series_count)
		samples = [series.values[groups == group_name] for group_name in group_names]
		box_look = BoxLook(color_codes[i], box_width, shows_outliers, series.name)
		draw_boxes(axes, samples, box_coordinates, box_look)

	position_count = len(coordinates)

	return position_count


def sort_groups(groups: NDArray[Any]) -> NDArray[Any]:
	"""
	Return each group once, in alphabetical order, without the missing one.

	.. versionadded:: 0.1.0

	Parameters
	----------
	groups
		The group of each row, None where it is missing.

	Returns
	-------
	NDArray
		The group names, in a numpy array of Python texts.

	Examples
	--------
	>>> import numpy
	>>> from numdaplot.plots.drawing.box_drawing import sort_groups
	>>> sort_groups(numpy.array(["Pau", None, "Lyon", "Pau"], dtype=object))
	array(['Lyon', 'Pau'], dtype=object)
	"""
	present = pandas.notna(groups)
	present_groups = groups[present]
	unique_groups = set[str](present_groups)
	sorted_groups = sorted(unique_groups)
	group_names = numpy.array(sorted_groups, dtype=TEXT_DTYPE)

	return group_names


def draw_boxes(
	axes: Axes, samples: list[NDArray[numpy.float64]], coordinates: NDArray[numpy.float64], box_look: BoxLook
) -> None:
	"""
	Draw the boxes of one column, one per sample, skipping the samples without value.

	.. versionadded:: 0.1.0

	Parameters
	----------
	axes
		The matplotlib axes drawn on.
	samples
		The numbers of each box, NaN where a value is missing.
	coordinates
		The middle of each box along the horizontal axis.
	box_look
		The color, the width, the outliers and the legend name of the boxes.

	Examples
	--------
	>>> import numpy
	>>> from matplotlib.figure import Figure
	>>> from numdaplot.plots.drawing.box_drawing import BoxLook, draw_boxes
	>>> axes = Figure().add_subplot()
	>>> samples = [numpy.array([1.0, 2.0, 4.0]), numpy.array([numpy.nan])]
	>>> draw_boxes(axes, samples, numpy.array([0.0, 1.0]), BoxLook("#1f77b4", 0.8, True, None))
	>>> len(axes.patches)
	1
	"""
	present_samples = [drop_missing_numbers(sample) for sample in samples]
	drawn_numbers = [i for i, sample in enumerate(present_samples) if sample.size > 0]
	drawn_count = len(drawn_numbers)
	if drawn_count == 0:
		return

	drawn_samples = [present_samples[i] for i in drawn_numbers]
	drawn_coordinates = coordinates[drawn_numbers]
	color_code = box_look.color_code
	box_style = {"facecolor": color_code, "edgecolor": color_code}
	line_style = {"color": color_code}
	median_style = {"color": BACKGROUND_COLOR, "linewidth": MEDIAN_LINE_WIDTH}
	outlier_style = {
		"marker": OUTLIER_MARKER,
		"markerfacecolor": color_code,
		"markeredgecolor": color_code,
		"markersize": OUTLIER_SIZE,
	}
	axes.boxplot(
		drawn_samples,
		positions=drawn_coordinates,
		widths=box_look.width,
		patch_artist=True,
		showfliers=box_look.shows_outliers,
		manage_ticks=False,
		label=box_look.label,
		boxprops=box_style,
		whiskerprops=line_style,
		capprops=line_style,
		medianprops=median_style,
		flierprops=outlier_style,
	)
