"""
Functional tests of the color scales of a HeatmapChart and of a ScatterChart.

.. versionadded:: 0.1.0
"""

# The matplotlib stubs leave the keyword arguments of most drawing methods untyped.
# pyright: reportUnknownMemberType=false

from typing import cast

import pytest
from matplotlib.collections import PathCollection, QuadMesh

import numdaplot as ndp

FLATS = ndp.Table.from_arrays(
	{
		"surface": ndp.Array.from_list([30.0, 45.0, 60.0]),
		"rooms": ndp.Array.from_list([1.0, 2.0, 3.0]),
		"change": ndp.Array.from_list([-1.0, 0.5, 4.0]),
		"city": ndp.Array.from_list(["Paris", "Lyon", "Paris"]),
		"sold": ndp.Array.from_list([True, False, True]),
	}
)
SCALE_NAMES = [
	(ndp.ColorScale.VIRIDIS, "viridis"),
	(ndp.ColorScale.BLUES, "Blues"),
	(ndp.ColorScale.REDS, "Reds"),
	(ndp.ColorScale.RED_BLUE, "RdBu_r"),
	(ndp.ColorScale.GREENS, "Greens"),
	(ndp.ColorScale.GRAYS, "Greys"),
	(ndp.ColorScale.CIVIDIS, "cividis"),
]
VISIBLE_COLOR_LIMIT = 0.9
REFUSED_TEXT_MESSAGE = "ScatterChart does not accept scale without a color_by column of numbers."
REFUSED_ALONE_MESSAGE = "ScatterChart does not accept scale without color_by."


def draw_scaled_points(chart: ndp.ScatterChart) -> PathCollection:
	"""
	Return the points of a scatter plot of the flats.

	.. versionadded:: 0.1.0

	Parameters
	----------
	chart
		The chart.

	Returns
	-------
	PathCollection
		The drawn points.
	"""
	figure = ndp.plot_scatter(FLATS, chart).to_matplotlib()
	points = cast(PathCollection, figure.axes[0].collections[0])

	return points


@pytest.mark.parametrize(("scale", "scale_name"), SCALE_NAMES)
def test_a_heatmap_uses_every_scale(scale: ndp.ColorScale, scale_name: str) -> None:
	"""
	Check the colors of a heatmap for each scale.

	.. versionadded:: 0.1.0

	Parameters
	----------
	scale
		The scale.
	scale_name
		Its matplotlib name.
	"""
	plot = ndp.plot_heatmap(FLATS, ndp.HeatmapChart(columns=["rooms"], scale=scale))

	image = plot.to_matplotlib().axes[0].images[0]

	assert image.get_cmap().name.startswith(scale_name)


@pytest.mark.parametrize(("scale", "scale_name"), SCALE_NAMES)
def test_points_use_every_scale(scale: ndp.ColorScale, scale_name: str) -> None:
	"""
	Check the colors of points for each scale.

	.. versionadded:: 0.1.0

	Parameters
	----------
	scale
		The scale.
	scale_name
		Its matplotlib name.
	"""
	chart = ndp.ScatterChart(x="surface", y="surface", color_by="rooms", scale=scale)

	points = draw_scaled_points(chart)

	assert points.get_cmap().name == scale_name


def test_points_use_viridis_by_default() -> None:
	"""
	Check that a chart without scale keeps its colors.

	.. versionadded:: 0.1.0
	"""
	points = draw_scaled_points(ndp.ScatterChart(x="surface", y="surface", color_by="rooms"))

	assert points.get_cmap().name == "viridis"


def test_red_blue_centers_points_on_zero() -> None:
	"""
	Check that white means 0 for points, as for a heatmap.

	.. versionadded:: 0.1.0
	"""
	chart = ndp.ScatterChart(x="surface", y="surface", color_by="change", scale=ndp.ColorScale.RED_BLUE)

	points = draw_scaled_points(chart)

	limits = [float(limit) for limit in points.get_clim()]
	assert limits == [-4.0, 4.0]


def test_the_color_bar_follows_the_scale_of_points() -> None:
	"""
	Check that the color bar shows the scale chosen.

	.. versionadded:: 0.1.0
	"""
	chart = ndp.ScatterChart(x="surface", y="surface", color_by="rooms", scale=ndp.ColorScale.GRAYS)

	figure = ndp.plot_scatter(FLATS, chart).to_matplotlib()

	color_bar_collections = figure.axes[1].collections
	color_bar_solids = [collection for collection in color_bar_collections if isinstance(collection, QuadMesh)]
	assert color_bar_solids[0].get_cmap().name == "Greys"


def test_a_scale_without_color_by_is_refused() -> None:
	"""
	Check the refusal when the chart is created.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(ndp.RefusedSettingError) as error_info:
		ndp.ScatterChart(scale=ndp.ColorScale.BLUES)

	error_text = str(error_info.value)
	assert error_text == REFUSED_ALONE_MESSAGE


@pytest.mark.parametrize("column", ["city", "sold"])
def test_a_scale_on_texts_or_booleans_is_refused(column: str) -> None:
	"""
	Check the refusal for columns taking one color per value.

	.. versionadded:: 0.1.0

	Parameters
	----------
	column
		The ``color_by`` column.
	"""
	chart = ndp.ScatterChart(x="surface", y="surface", color_by=column, scale=ndp.ColorScale.BLUES)

	with pytest.raises(ndp.RefusedSettingError) as error_info:
		ndp.plot_scatter(FLATS, chart)

	error_text = str(error_info.value)
	assert error_text == REFUSED_TEXT_MESSAGE


def test_add_scatter_refuses_a_scale_on_texts() -> None:
	"""
	Check the same refusal for points drawn over a Plot.

	.. versionadded:: 0.1.0
	"""
	line_plot = ndp.plot_line(FLATS, ndp.LineChart(x="surface", y=["rooms"]))
	chart = ndp.ScatterChart(x="surface", y="rooms", color_by="city", scale=ndp.ColorScale.BLUES)

	with pytest.raises(ndp.RefusedSettingError):
		line_plot.add_scatter(FLATS, chart)


@pytest.mark.parametrize(
	"scale",
	[ndp.ColorScale.BLUES, ndp.ColorScale.REDS, ndp.ColorScale.GREENS, ndp.ColorScale.GRAYS],
)
def test_points_of_the_smallest_value_stay_visible(scale: ndp.ColorScale) -> None:
	"""
	Check that a scale starting from white gives points a visible color, and its bar the same one.

	.. versionadded:: 0.1.0

	Parameters
	----------
	scale
		The scale.
	"""
	chart = ndp.ScatterChart(x="surface", y="surface", color_by="rooms", scale=scale)

	figure = ndp.plot_scatter(FLATS, chart).to_matplotlib()

	points = cast(PathCollection, figure.axes[0].collections[0])
	first_color = points.get_cmap()(0.0)
	color_bar_collections = figure.axes[1].collections
	color_bar_solids = [collection for collection in color_bar_collections if isinstance(collection, QuadMesh)]
	first_bar_color = color_bar_solids[0].get_cmap()(0.0)
	assert min(first_color[:3]) < VISIBLE_COLOR_LIMIT
	assert first_bar_color == first_color


def test_a_heatmap_keeps_the_white_of_its_scale() -> None:
	"""
	Check that a cell of the smallest value stays almost white.

	.. versionadded:: 0.1.0
	"""
	plot = ndp.plot_heatmap(FLATS, ndp.HeatmapChart(columns=["rooms"], scale=ndp.ColorScale.BLUES))

	image = plot.to_matplotlib().axes[0].images[0]

	first_color = image.get_cmap()(0.0)
	assert min(first_color[:3]) > VISIBLE_COLOR_LIMIT


def test_red_blue_keeps_white_for_zero_on_points() -> None:
	"""
	Check that the middle of RED_BLUE stays white on points.

	.. versionadded:: 0.1.0
	"""
	chart = ndp.ScatterChart(x="surface", y="surface", color_by="change", scale=ndp.ColorScale.RED_BLUE)

	points = draw_scaled_points(chart)

	middle_color = points.get_cmap()(0.5)
	assert min(middle_color[:3]) > VISIBLE_COLOR_LIMIT
