"""
Functional tests of the opacity and the size of the points of a ScatterChart.

.. versionadded:: 0.1.0
"""

# The matplotlib stubs leave the keyword arguments of most drawing methods untyped.
# pyright: reportUnknownMemberType=false

import math
from typing import cast

import pytest
from matplotlib.collections import PathCollection, QuadMesh
from matplotlib.figure import Figure

import numdaplot as ndp

OPACITY = 0.25
POINT_SIZE = 3.0
POINT_AREA = 9.0
DEFAULT_AREA = 36.0
FLATS = ndp.Table.from_arrays(
	{
		"surface": ndp.Array.from_list([30.0, 45.0, 60.0]),
		"price": ndp.Array.from_list([150.0, 210.0, 260.0]),
		"city": ndp.Array.from_list(["Paris", "Lyon", "Paris"]),
		"rooms": ndp.Array.from_list([1.0, 2.0, 3.0]),
	}
)


def draw_points(chart: ndp.ScatterChart) -> Figure:
	"""
	Return the figure of a scatter plot of the flats.

	.. versionadded:: 0.1.0

	Parameters
	----------
	chart
		The chart.

	Returns
	-------
	Figure
		The drawn figure.
	"""
	plot = ndp.Plot.scatter(FLATS, chart)
	figure = plot.to_matplotlib()
	figure.draw_without_rendering()

	return figure


def test_points_are_opaque_with_the_default_size_by_default() -> None:
	"""
	Check that a chart without these settings keeps its look.

	.. versionadded:: 0.1.0
	"""
	figure = draw_points(ndp.ScatterChart(x="surface", y="price"))

	points = cast(PathCollection, figure.axes[0].collections[0])
	assert points.get_alpha() == 1.0
	assert points.get_sizes().tolist() == [DEFAULT_AREA] * 3


def test_opacity_and_point_size_apply_to_a_single_color() -> None:
	"""
	Check both settings on points of one color.

	.. versionadded:: 0.1.0
	"""
	figure = draw_points(ndp.ScatterChart(x="surface", y="price", opacity=OPACITY, point_size=POINT_SIZE))

	points = cast(PathCollection, figure.axes[0].collections[0])
	assert points.get_alpha() == OPACITY
	assert points.get_sizes().tolist() == [POINT_AREA] * 3


def test_opacity_and_point_size_apply_to_every_group() -> None:
	"""
	Check both settings on each group of ``color_by`` texts.

	.. versionadded:: 0.1.0
	"""
	chart = ndp.ScatterChart(x="surface", y="price", color_by="city", opacity=OPACITY, point_size=POINT_SIZE)

	figure = draw_points(chart)

	groups = cast(list[PathCollection], list(figure.axes[0].collections))
	assert [group.get_alpha() for group in groups] == [OPACITY, OPACITY]
	assert groups[0].get_sizes()[0] == POINT_AREA


def test_the_legend_stays_opaque() -> None:
	"""
	Check that transparent points keep a readable legend.

	.. versionadded:: 0.1.0
	"""
	chart = ndp.ScatterChart(x="surface", y="price", color_by="city", opacity=OPACITY)

	figure = draw_points(chart)

	legend = figure.axes[0].get_legend()
	assert legend is not None
	handles = cast(list[PathCollection], list(legend.legend_handles))
	assert [handle.get_alpha() for handle in handles] == [1.0, 1.0]


def test_a_color_scale_keeps_an_opaque_bar() -> None:
	"""
	Check that transparent points colored by numbers keep a readable color bar.

	.. versionadded:: 0.1.0
	"""
	chart = ndp.ScatterChart(x="surface", y="price", color_by="rooms", opacity=OPACITY)

	figure = draw_points(chart)

	points = cast(PathCollection, figure.axes[0].collections[0])
	color_bar_axes = figure.axes[1]
	color_bar_solids = [collection for collection in color_bar_axes.collections if isinstance(collection, QuadMesh)]
	assert points.get_alpha() == OPACITY
	assert color_bar_solids[0].get_alpha() is None


def test_size_by_keeps_its_sizes_with_an_opacity() -> None:
	"""
	Check that ``opacity`` combines with ``size_by``.

	.. versionadded:: 0.1.0
	"""
	chart = ndp.ScatterChart(x="surface", y="price", size_by="rooms", opacity=OPACITY)

	figure = draw_points(chart)

	points = cast(PathCollection, figure.axes[0].collections[0])
	assert points.get_alpha() == OPACITY
	assert points.get_sizes().tolist() == [16.0, 136.0, 256.0]


def test_add_scatter_uses_the_settings() -> None:
	"""
	Check both settings on points drawn over a Plot.

	.. versionadded:: 0.1.0
	"""
	line_plot = ndp.Plot.line(FLATS, ndp.LineChart(x="surface", y=["price"]))
	chart = ndp.ScatterChart(x="surface", y="price", opacity=OPACITY, point_size=POINT_SIZE)

	both = line_plot.add_scatter(FLATS, chart)

	figure = both.to_matplotlib()
	points = cast(PathCollection, figure.axes[0].collections[0])
	assert points.get_alpha() == OPACITY
	assert points.get_sizes()[0] == POINT_AREA


def test_point_size_and_size_by_are_refused_together() -> None:
	"""
	Check that a chart has only one source for the size of its points.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(ndp.ConflictingSettingsError):
		ndp.ScatterChart(size_by="rooms", point_size=POINT_SIZE)


@pytest.mark.parametrize("opacity", [0.0, -0.5, 1.5, math.nan])
def test_an_opacity_that_cannot_be_drawn_is_refused(opacity: float) -> None:
	"""
	Check the refused opacities.

	.. versionadded:: 0.1.0

	Parameters
	----------
	opacity
		The opacity.
	"""
	with pytest.raises(ndp.InvalidOpacityError):
		ndp.ScatterChart(opacity=opacity)


@pytest.mark.parametrize("opacity", [0.01, 1, 1.0])
def test_an_opacity_up_to_one_is_accepted(opacity: float) -> None:
	"""
	Check the accepted limits of an opacity.

	.. versionadded:: 0.1.0

	Parameters
	----------
	opacity
		The opacity.
	"""
	chart = ndp.ScatterChart(opacity=opacity)

	assert chart.opacity == opacity


@pytest.mark.parametrize("point_size", [0.0, -1.0, math.inf, math.nan])
def test_a_point_size_that_cannot_be_drawn_is_refused(point_size: float) -> None:
	"""
	Check the refused sizes.

	.. versionadded:: 0.1.0

	Parameters
	----------
	point_size
		The size.
	"""
	with pytest.raises(ndp.InvalidPointSizeError):
		ndp.ScatterChart(point_size=point_size)


@pytest.mark.parametrize(
	"settings",
	[{"opacity": "high"}, {"point_size": "big"}],
)
def test_settings_of_the_wrong_type_are_refused(settings: dict[str, str]) -> None:
	"""
	Check the type of both settings.

	.. versionadded:: 0.1.0

	Parameters
	----------
	settings
		The settings.
	"""
	with pytest.raises(ndp.InvalidTypeError):
		ndp.ScatterChart(**settings)  # type: ignore[arg-type]
