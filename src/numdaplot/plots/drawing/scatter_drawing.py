"""
Drawing of a ScatterChart.

.. versionadded:: 0.1.0
"""

# The matplotlib stubs leave the keyword arguments of most drawing methods untyped.
# pyright: reportUnknownMemberType=false

from dataclasses import dataclass
from typing import Any, cast

import numpy
import pandas
from matplotlib.axes import Axes
from matplotlib.collections import PathCollection
from numpy.typing import NDArray

from numdaplot.ordering.natural_order import find_natural_key
from numdaplot.plots.chart_layer import ChartLayer
from numdaplot.plots.charts.color_scale import ColorScale
from numdaplot.plots.charts.scatter_chart import ScatterChart
from numdaplot.plots.data.chart_values import ChartValues, Series
from numdaplot.plots.data.point_values import PointValues
from numdaplot.plots.drawing.color_bar import add_color_bar
from numdaplot.plots.drawing.color_scale_values import find_point_colors, find_scale_limits
from numdaplot.plots.drawing.colored_parts import ColoredParts
from numdaplot.plots.drawing.default_labels import find_position_label
from numdaplot.plots.drawing.drawn_chart import DrawnChart
from numdaplot.plots.drawing.grid_axes import GridAxes
from numdaplot.plots.drawing.marker_codes import MARKER_CODES
from numdaplot.plots.drawing.position_axis import place_positions
from numdaplot.plots.drawing.series_colors import choose_series_colors
from numdaplot.plots.style.color import Color
from numdaplot.plots.style.custom_color import CustomColor

CHART_NAME = "ScatterChart"
DEFAULT_POINT_SIZE = 6.0
SMALLEST_POINT_AREA = 16.0
LARGEST_POINT_AREA = 256.0
DEFAULT_COLOR_SCALE = ColorScale.VIRIDIS
NO_POINT_VALUES = PointValues(None, None, None, None)


@dataclass(frozen=True, eq=False)
class PointLook:
	"""
	The look shared by the points of a ScatterChart.

	.. versionadded:: 0.1.0

	Parameters
	----------
	coordinates
		The coordinates of the ``x`` values.
	areas
		The area of each point in square points.
	marker_code
		The matplotlib code of the marker shape.
	opacity
		How opaque the points are, from 0 to 1.
	scale
		The colors of the points colored by numbers.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> import numpy
	>>> from numdaplot.plots.drawing.scatter_drawing import PointLook
	>>> PointLook(numpy.array([0.0]), numpy.array([36.0]), "o", 1.0, ndp.ColorScale.VIRIDIS).marker_code
	'o'
	"""

	coordinates: NDArray[Any]
	areas: NDArray[numpy.float64]
	marker_code: str
	opacity: float
	scale: ColorScale


def draw_scatter_chart(axes: Axes, layer: ChartLayer) -> DrawnChart:
	"""
	Draw each row of a ScatterChart as a point, colored and sized by the ``color_by`` and ``size_by`` columns.

	.. versionadded:: 0.1.0

	Parameters
	----------
	axes
		The matplotlib axes drawn on.
	layer
		A ScatterChart, its values and the values of its points.

	Returns
	-------
	DrawnChart
		The default labels, grid lines across both axes, and the ``color_by`` column as legend title when it
		holds texts.

	Raises
	------
	InvalidColorCountError
		When ``color`` is given for an Array of several columns.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> from matplotlib.figure import Figure
	>>> from numdaplot.plots.chart_layer import ChartLayer
	>>> from numdaplot.plots.data.array_values import read_array_values
	>>> from numdaplot.plots.drawing.scatter_drawing import draw_scatter_chart
	>>> prices = ndp.Array.from_list([12.0, 15.5])
	>>> axes = Figure().add_subplot()
	>>> layer = ChartLayer(ndp.ScatterChart(), read_array_values(prices, "ScatterChart"))
	>>> drawn_chart = draw_scatter_chart(axes, layer)
	>>> axes.collections[0].get_offsets().tolist()
	[[0.0, 12.0], [1.0, 15.5]]
	"""
	chart = cast(ScatterChart, layer.chart)
	values = cast(ChartValues, layer.values)
	points = NO_POINT_VALUES
	if layer.points is not None:
		points = layer.points

	coordinates = place_positions(axes, values.positions, False)
	row_count = len(coordinates)
	areas = choose_areas(points.sizes, row_count, chart.point_size)
	marker_code = MARKER_CODES[chart.marker]
	scale = DEFAULT_COLOR_SCALE if chart.scale is None else chart.scale
	point_look = PointLook(coordinates, areas, marker_code, chart.opacity, scale)
	x_label = find_position_label(values.positions)
	no_legend_chart = DrawnChart(x_label, values.value_name, False, GridAxes.BOTH, None)
	if points.colors is None:
		draw_colored_series(axes, chart.color, values.series, point_look)
		return no_legend_chart

	color_name = cast(str, points.color_name)
	first_series = values.series[0]
	if points.colors.dtype == numpy.float64:
		scaled_points = draw_color_scale(axes, first_series, points.colors, point_look)
		add_color_bar(axes, scaled_points, color_name, points.colors)
		return no_legend_chart

	draw_color_groups(axes, first_series, points, point_look)
	group_chart = DrawnChart(x_label, values.value_name, False, GridAxes.BOTH, color_name)

	return group_chart


def choose_areas(
	sizes: NDArray[numpy.float64] | None, row_count: int, point_size: float | None
) -> NDArray[numpy.float64]:
	"""
	Return the area of each point, scaled from the smallest to the largest ``size_by`` value.

	.. versionadded:: 0.1.0

	Parameters
	----------
	sizes
		The ``size_by`` values, NaN where a value is missing, or None for points of the same size.
	row_count
		The number of points.
	point_size
		The diameter of every point without ``size_by``, or None for the default diameter.

	Returns
	-------
	NDArray[numpy.float64]
		Areas from 16 to 256 square points, the square of the diameter for every point without ``size_by``, 36 by
		default, and the middle area when every value is the same. A point with a missing size is not drawn, its area
		is 0.

	Examples
	--------
	>>> import numpy
	>>> from numdaplot.plots.drawing.scatter_drawing import choose_areas
	>>> choose_areas(numpy.array([10.0, 20.0, 30.0]), 3, None)
	array([ 16., 136., 256.])
	"""
	if sizes is None:
		diameter = DEFAULT_POINT_SIZE if point_size is None else point_size
		same_areas = numpy.full(row_count, diameter**2)
		return same_areas

	area_range = LARGEST_POINT_AREA - SMALLEST_POINT_AREA
	middle_area = SMALLEST_POINT_AREA + area_range / 2
	present = ~numpy.isnan(sizes)
	present_sizes = sizes[present]
	areas = numpy.full(row_count, middle_area)
	present_count = len(present_sizes)
	if present_count == 0:
		return areas

	smallest_size = present_sizes.min()
	largest_size = present_sizes.max()
	size_range = largest_size - smallest_size
	if size_range > 0:
		size_shares = (sizes - smallest_size) / size_range
		areas = SMALLEST_POINT_AREA + size_shares * area_range

	drawn_areas = numpy.where(present, areas, 0.0)

	return drawn_areas


def draw_colored_series(
	axes: Axes, color: Color | CustomColor | None, series_list: list[Series], point_look: PointLook
) -> None:
	"""
	Draw the points of each series in one color.

	.. versionadded:: 0.1.0

	Parameters
	----------
	axes
		The matplotlib axes drawn on.
	color
		The color of the points of a single series, or None for the colors of the default cycle.
	series_list
		The series drawn.
	point_look
		The coordinates, the areas and the marker of the points.

	Raises
	------
	InvalidColorCountError
		When a color is given for several series.

	Examples
	--------
	>>> import numpy
	>>> import numdaplot as ndp
	>>> from matplotlib.figure import Figure
	>>> from numdaplot.plots.data.chart_values import Series
	>>> from numdaplot.plots.drawing.scatter_drawing import PointLook, draw_colored_series
	>>> axes = Figure().add_subplot()
	>>> point_look = PointLook(numpy.array([0.0]), numpy.array([36.0]), "o", 1.0, ndp.ColorScale.VIRIDIS)
	>>> draw_colored_series(axes, ndp.Color.RED, [Series("price", numpy.array([12.0]))], point_look)
	>>> axes.collections[0].get_facecolor().round(2).tolist()
	[[0.84, 0.15, 0.16, 1.0]]
	"""
	chosen_colors = None
	if color is not None:
		chosen_colors = [color]

	series_count = len(series_list)
	color_codes = choose_series_colors(chosen_colors, series_count, CHART_NAME, ColoredParts.SERIES)

	for series, color_code in zip(series_list, color_codes, strict=True):
		axes.scatter(
			point_look.coordinates,
			series.values,
			s=point_look.areas,
			color=color_code,
			marker=point_look.marker_code,
			alpha=point_look.opacity,
			label=series.name,
		)


def draw_color_scale(
	axes: Axes, series: Series, color_numbers: NDArray[numpy.float64], point_look: PointLook
) -> PathCollection:
	"""
	Draw points colored along a color scale, from the smallest to the largest ``color_by`` number.

	.. versionadded:: 0.1.0

	Parameters
	----------
	axes
		The matplotlib axes drawn on.
	series
		The series drawn.
	color_numbers
		The ``color_by`` numbers.
	point_look
		The coordinates, the areas and the marker of the points.

	Returns
	-------
	matplotlib.collections.PathCollection
		The drawn points, which the color bar describes.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> import numpy
	>>> from matplotlib.figure import Figure
	>>> from numdaplot.plots.data.chart_values import Series
	>>> from numdaplot.plots.drawing.scatter_drawing import PointLook, draw_color_scale
	>>> axes = Figure().add_subplot()
	>>> point_look = PointLook(numpy.array([0.0, 1.0]), numpy.array([36.0, 36.0]), "o", 1.0, ndp.ColorScale.VIRIDIS)
	>>> series = Series("price", numpy.array([1.0, 2.0]))
	>>> scaled_points = draw_color_scale(axes, series, numpy.array([5.0, 9.0]), point_look)
	>>> [float(limit) for limit in scaled_points.get_clim()]
	[5.0, 9.0]
	"""
	point_colors = find_point_colors(point_look.scale)
	lowest_color, highest_color = find_scale_limits(color_numbers, point_look.scale)
	scaled_points = axes.scatter(
		point_look.coordinates,
		series.values,
		s=point_look.areas,
		c=color_numbers,
		cmap=point_colors,
		vmin=lowest_color,
		vmax=highest_color,
		marker=point_look.marker_code,
		alpha=point_look.opacity,
	)

	return scaled_points


def draw_color_groups(axes: Axes, series: Series, points: PointValues, point_look: PointLook) -> None:
	"""
	Draw the points of each ``color_by`` text in its own color, named in the legend.

	The texts take the colors of the default cycle in the order ``order_color_groups`` gives.

	.. versionadded:: 0.1.0
	.. versionchanged:: 0.2.0
		Takes the values of the points, and draws the texts in natural order, or in the order of the categories.

	Parameters
	----------
	axes
		The matplotlib axes drawn on.
	series
		The series drawn.
	points
		The values of the points: the ``color_by`` texts, None where a text is missing, and the order of their
		categories.
	point_look
		The coordinates, the areas and the marker of the points.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> import numpy
	>>> from matplotlib.figure import Figure
	>>> from numdaplot.plots.data.chart_values import Series
	>>> from numdaplot.plots.data.point_values import PointValues
	>>> from numdaplot.plots.drawing.scatter_drawing import PointLook, draw_color_groups
	>>> axes = Figure().add_subplot()
	>>> point_look = PointLook(numpy.array([0.0, 1.0]), numpy.array([36.0, 36.0]), "o", 1.0, ndp.ColorScale.VIRIDIS)
	>>> points = PointValues("city", numpy.array(["Pau", "Lyon"], dtype=object), None, None)
	>>> draw_color_groups(axes, Series("price", numpy.array([1.0, 2.0])), points, point_look)
	>>> [drawn_points.get_label() for drawn_points in axes.collections]
	['Lyon', 'Pau']
	"""
	color_texts = cast(NDArray[Any], points.colors)
	present = pandas.notna(color_texts)
	present_texts = color_texts[present]
	groups = order_color_groups(present_texts, points.color_order)
	group_count = len(groups)
	color_codes = choose_series_colors(None, group_count, CHART_NAME, ColoredParts.COLOR_GROUPS)

	for group, color_code in zip(groups, color_codes, strict=True):
		in_group = color_texts == group
		axes.scatter(
			point_look.coordinates[in_group],
			series.values[in_group],
			s=point_look.areas[in_group],
			color=color_code,
			marker=point_look.marker_code,
			alpha=point_look.opacity,
			label=group,
		)


def order_color_groups(present_texts: NDArray[Any], color_order: list[str] | None) -> list[str]:
	"""
	Return each ``color_by`` text once, in the order of the legend.

	Categories keep the order of the column, without the categories no point holds. Any other texts are sorted in
	natural order: numbers inside them as numbers, without regard to case.

	.. versionadded:: 0.2.0

	Parameters
	----------
	present_texts
		The ``color_by`` texts of the drawn points, without missing text.
	color_order
		The texts of the categories in their order, or None for texts that are not categories.

	Returns
	-------
	list[str]
		The texts of the groups, each once.

	Examples
	--------
	>>> import numpy
	>>> from numdaplot.plots.drawing.scatter_drawing import order_color_groups
	>>> order_color_groups(numpy.array(["Noise", "Cluster 10", "Cluster 2"], dtype=object), None)
	['Cluster 2', 'Cluster 10', 'Noise']
	>>> order_color_groups(numpy.array(["10 to 99"], dtype=object), ["0 to 9", "10 to 99"])
	['10 to 99']
	"""
	raw_texts = present_texts.tolist()
	group_texts = set(cast(list[str], raw_texts))
	if color_order is not None:
		held_categories = [category for category in color_order if category in group_texts]
		return held_categories

	sorted_groups = sorted(group_texts, key=find_natural_key)

	return sorted_groups
