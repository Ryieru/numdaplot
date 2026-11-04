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
from matplotlib.figure import Figure
from numpy.typing import NDArray

from numdaplot.plots.chart_layer import ChartLayer
from numdaplot.plots.charts.scatter_chart import ScatterChart
from numdaplot.plots.data.chart_values import Series
from numdaplot.plots.data.point_values import PointValues
from numdaplot.plots.drawing.drawn_chart import DrawnChart
from numdaplot.plots.drawing.marker_codes import MARKER_CODES
from numdaplot.plots.drawing.position_axis import place_positions
from numdaplot.plots.drawing.series_colors import choose_series_colors
from numdaplot.plots.drawing.whole_numbers import place_whole_ticks
from numdaplot.plots.style.color import Color
from numdaplot.plots.style.custom_color import CustomColor

DEFAULT_POINT_AREA = 36.0
SMALLEST_POINT_AREA = 16.0
LARGEST_POINT_AREA = 256.0
COLOR_SCALE = "viridis"
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

	Examples
	--------
	>>> import numpy
	>>> from numdaplot.plots.drawing.scatter_drawing import PointLook
	>>> PointLook(numpy.array([0.0]), numpy.array([36.0]), "o").marker_code
	'o'
	"""

	coordinates: NDArray[Any]
	areas: NDArray[numpy.float64]
	marker_code: str


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
	values = layer.values
	points = NO_POINT_VALUES
	if layer.points is not None:
		points = layer.points

	coordinates = place_positions(axes, values.positions, False)
	row_count = len(coordinates)
	areas = choose_areas(points.sizes, row_count)
	marker_code = MARKER_CODES[chart.marker]
	point_look = PointLook(coordinates, areas, marker_code)
	no_legend_chart = DrawnChart(values.positions.name, values.value_name, False, True, None)
	if points.colors is None:
		draw_colored_series(axes, chart.color, values.series, point_look)
		return no_legend_chart

	color_name = cast(str, points.color_name)
	first_series = values.series[0]
	if points.colors.dtype == numpy.float64:
		scaled_points = draw_color_scale(axes, first_series, points.colors, point_look)
		add_color_bar(axes, scaled_points, color_name, points.colors)
		return no_legend_chart

	draw_color_groups(axes, first_series, points.colors, point_look)
	group_chart = DrawnChart(values.positions.name, values.value_name, False, True, color_name)

	return group_chart


def choose_areas(sizes: NDArray[numpy.float64] | None, row_count: int) -> NDArray[numpy.float64]:
	"""
	Return the area of each point, scaled from the smallest to the largest ``size_by`` value.

	.. versionadded:: 0.1.0

	Parameters
	----------
	sizes
		The ``size_by`` values, NaN where a value is missing, or None for points of the same size.
	row_count
		The number of points.

	Returns
	-------
	NDArray[numpy.float64]
		Areas from 16 to 256 square points, 36 for every point without ``size_by``, and the middle area when
		every value is the same. A point with a missing size is not drawn, its area is 0.

	Examples
	--------
	>>> import numpy
	>>> from numdaplot.plots.drawing.scatter_drawing import choose_areas
	>>> choose_areas(numpy.array([10.0, 20.0, 30.0]), 3)
	array([ 16., 136., 256.])
	"""
	if sizes is None:
		default_areas = numpy.full(row_count, DEFAULT_POINT_AREA)
		return default_areas

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
	>>> point_look = PointLook(numpy.array([0.0]), numpy.array([36.0]), "o")
	>>> draw_colored_series(axes, ndp.Color.RED, [Series("price", numpy.array([12.0]))], point_look)
	>>> axes.collections[0].get_facecolor().round(2).tolist()
	[[0.84, 0.15, 0.16, 1.0]]
	"""
	chosen_colors = None
	if color is not None:
		chosen_colors = [color]

	series_count = len(series_list)
	color_codes = choose_series_colors(chosen_colors, series_count)

	for series, color_code in zip(series_list, color_codes, strict=True):
		axes.scatter(
			point_look.coordinates,
			series.values,
			s=point_look.areas,
			color=color_code,
			marker=point_look.marker_code,
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
	>>> import numpy
	>>> from matplotlib.figure import Figure
	>>> from numdaplot.plots.data.chart_values import Series
	>>> from numdaplot.plots.drawing.scatter_drawing import PointLook, draw_color_scale
	>>> axes = Figure().add_subplot()
	>>> point_look = PointLook(numpy.array([0.0, 1.0]), numpy.array([36.0, 36.0]), "o")
	>>> series = Series("price", numpy.array([1.0, 2.0]))
	>>> scaled_points = draw_color_scale(axes, series, numpy.array([5.0, 9.0]), point_look)
	>>> [float(limit) for limit in scaled_points.get_clim()]
	[5.0, 9.0]
	"""
	scaled_points = axes.scatter(
		point_look.coordinates,
		series.values,
		s=point_look.areas,
		c=color_numbers,
		cmap=COLOR_SCALE,
		marker=point_look.marker_code,
	)

	return scaled_points


def add_color_bar(
	axes: Axes, scaled_points: PathCollection, color_name: str, color_numbers: NDArray[numpy.float64]
) -> None:
	"""
	Draw the color scale of the points next to the axes, labeled with the ``color_by`` column.

	Its ticks are on whole numbers only when every ``color_by`` number is whole.

	.. versionadded:: 0.1.0

	Parameters
	----------
	axes
		The matplotlib axes drawn on.
	scaled_points
		The points colored along the scale.
	color_name
		The ``color_by`` column.
	color_numbers
		The ``color_by`` numbers.

	Examples
	--------
	>>> import numpy
	>>> from matplotlib.figure import Figure
	>>> from numdaplot.plots.drawing.scatter_drawing import add_color_bar
	>>> figure = Figure()
	>>> axes = figure.add_subplot()
	>>> add_color_bar(axes, axes.scatter([0.0], [1.0], c=[5.0]), "rooms", numpy.array([5.0]))
	>>> figure.axes[1].get_ylabel()
	'rooms'
	"""
	figure = cast(Figure, axes.figure)
	color_bar = figure.colorbar(scaled_points, ax=axes, label=color_name)
	place_whole_ticks(color_bar.ax.yaxis, color_numbers)


def draw_color_groups(axes: Axes, series: Series, color_texts: NDArray[Any], point_look: PointLook) -> None:
	"""
	Draw the points of each ``color_by`` text in its own color, named in the legend.

	The texts take the colors of the default cycle in the order they first appear.

	.. versionadded:: 0.1.0

	Parameters
	----------
	axes
		The matplotlib axes drawn on.
	series
		The series drawn.
	color_texts
		The ``color_by`` texts, None where a text is missing.
	point_look
		The coordinates, the areas and the marker of the points.

	Examples
	--------
	>>> import numpy
	>>> from matplotlib.figure import Figure
	>>> from numdaplot.plots.data.chart_values import Series
	>>> from numdaplot.plots.drawing.scatter_drawing import PointLook, draw_color_groups
	>>> axes = Figure().add_subplot()
	>>> point_look = PointLook(numpy.array([0.0, 1.0]), numpy.array([36.0, 36.0]), "o")
	>>> texts = numpy.array(["Pau", "Lyon"], dtype=object)
	>>> draw_color_groups(axes, Series("price", numpy.array([1.0, 2.0])), texts, point_look)
	>>> [points.get_label() for points in axes.collections]
	['Pau', 'Lyon']
	"""
	present = pandas.notna(color_texts)
	present_texts = color_texts[present]
	groups = pandas.unique(present_texts)
	group_count = len(groups)
	color_codes = choose_series_colors(None, group_count)

	for group, color_code in zip(groups, color_codes, strict=True):
		in_group = color_texts == group
		axes.scatter(
			point_look.coordinates[in_group],
			series.values[in_group],
			s=point_look.areas[in_group],
			color=color_code,
			marker=point_look.marker_code,
			label=group,
		)
