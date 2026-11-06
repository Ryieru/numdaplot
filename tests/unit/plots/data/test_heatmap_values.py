"""
Unit tests of the values of a HeatmapChart.

.. versionadded:: 0.1.0
"""

# The matplotlib stubs leave the keyword arguments of most drawing methods untyped.
# pyright: reportUnknownMemberType=false

import pytest

import numdaplot as ndp
from numdaplot.plots.data.heatmap_values import read_heatmap_values

DAYS = ndp.Array.from_list([1, 2, 3])
PRICES = ndp.Array.from_list([12.0, 15.5, 14.0])
CITIES = ndp.Array.from_list(["Paris", "Lyon", "Paris"])
SALES = ndp.Table.from_arrays({"day": DAYS, "price": PRICES, "city": CITIES})
GRID = ndp.Array.from_list([[1.0, 2.0], [3.0, 4.0]])


def test_read_heatmap_values_reads_the_labels_and_columns_of_a_table() -> None:
	"""
	Check that labels gives the row positions and columns the series.

	.. versionadded:: 0.1.0
	"""
	values = read_heatmap_values(SALES, ndp.HeatmapChart(columns=["price"], labels="city"))

	assert values.positions.name == "city"
	assert values.series[0].name == "price"


def test_read_heatmap_values_rejects_a_table_without_columns() -> None:
	"""
	Check that a Table needs columns, named as the HeatmapChart names them.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(ndp.InvalidChartDataError, match="needs columns"):
		read_heatmap_values(SALES, ndp.HeatmapChart(labels="city"))


def test_read_heatmap_values_reads_each_column_of_an_array() -> None:
	"""
	Check that an Array gives one series per column.

	.. versionadded:: 0.1.0
	"""
	values = read_heatmap_values(GRID, ndp.HeatmapChart())

	series_count = len(values.series)
	assert series_count == 2
