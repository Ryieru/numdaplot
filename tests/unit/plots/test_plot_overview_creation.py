"""
Unit tests of the creation of a Plot giving an overview of values.

.. versionadded:: 0.1.0
"""

# The matplotlib stubs leave the keyword arguments of most drawing methods untyped.
# pyright: reportUnknownMemberType=false

from typing import Any, cast

import pytest

import numdaplot as ndp

PRICES = ndp.Array.from_list([12.0, 15.5, 14.0])
GRID = ndp.Array.from_list([[1.0, 2.0], [3.0, 4.0]])


def test_plot_heatmap_draws_with_the_default_style() -> None:
	"""
	Check that a heatmap without style has its default title.

	.. versionadded:: 0.1.0
	"""
	plot = ndp.Plot.heatmap(GRID, ndp.HeatmapChart())

	figure = plot.to_matplotlib()
	assert figure.axes[0].get_title() == "Row by Column"


def test_plot_missing_by_column_rejects_an_array() -> None:
	"""
	Check that an Array raises InvalidTypeError naming the method.

	.. versionadded:: 0.1.0
	"""
	untyped_plot = cast(Any, ndp.Plot.missing_by_column)

	with pytest.raises(ndp.InvalidTypeError, match="Plot.missing_by_column"):
		untyped_plot(PRICES, ndp.MissingChart())


def test_plot_missing_map_rejects_an_array() -> None:
	"""
	Check that an Array raises InvalidTypeError naming the method.

	.. versionadded:: 0.1.0
	"""
	untyped_plot = cast(Any, ndp.Plot.missing_map)

	with pytest.raises(ndp.InvalidTypeError, match="Plot.missing_map"):
		untyped_plot(PRICES)
