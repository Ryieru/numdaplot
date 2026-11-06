"""
Unit tests of the methods every creation of a Plot shares.

.. versionadded:: 0.1.0
"""

# The matplotlib stubs leave the keyword arguments of most drawing methods untyped.
# pyright: reportUnknownMemberType=false

from collections.abc import Callable

import pytest

import numdaplot as ndp

DAYS = ndp.Array.from_list([1, 2, 3])
PRICES = ndp.Array.from_list([12.0, 15.5, 14.0])
CITIES = ndp.Array.from_list(["Paris", "Lyon", "Paris"])
SALES = ndp.Table.from_arrays({"day": DAYS, "price": PRICES, "city": CITIES})
GRID = ndp.Array.from_list([[1.0, 2.0], [3.0, 4.0]])
MISSING_PRICES = ndp.Table.from_arrays({"price": ndp.Array.from_list([12.0, None])})


@pytest.mark.parametrize(
	("plot_creation", "data"),
	[
		(ndp.Plot.line, PRICES),
		(ndp.Plot.bar, PRICES),
		(ndp.Plot.scatter, PRICES),
		(ndp.Plot.box, PRICES),
		(ndp.Plot.histogram, PRICES),
		(ndp.Plot.heatmap, GRID),
		(ndp.Plot.missing_by_column, MISSING_PRICES),
	],
)
def test_plot_creation_without_chart_draws_with_the_default_chart(
	plot_creation: Callable[..., ndp.Plot],
	data: ndp.Table | ndp.Array,
) -> None:
	"""
	Check that a creation method called without chart draws one chart.

	.. versionadded:: 0.1.0

	Parameters
	----------
	plot_creation
		The creation method.
	data
		Data the default chart draws.
	"""
	plot = plot_creation(data)

	figure = plot.to_matplotlib()
	axes_count = len(figure.axes)
	assert axes_count >= 1


def test_plot_creation_without_chart_still_needs_the_columns_of_a_table() -> None:
	"""
	Check that a Table without chart raises InvalidChartDataError.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(ndp.InvalidChartDataError):
		ndp.Plot.bar(SALES)
